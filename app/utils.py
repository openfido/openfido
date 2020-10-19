import hashlib
import logging
import secrets
from datetime import datetime, timedelta, timezone
from calendar import timegm
from typing import Tuple

import jwt
import os
import boto3
from botocore.client import Config
from flask import current_app, has_request_context, request, g
from jwt.exceptions import PyJWTError

JWT_EXPIRATION_DAYS = 14
JWT_MAX_EXPIRATION_DAYS = 3 * JWT_EXPIRATION_DAYS
JWT_ALGORITHM = "HS256"

logger = logging.getLogger("auth")


class BadRequestError(ValueError):
    pass

def get_s3():
    """ Get access to the Boto s3 service. """

    params = {
        "endpoint_url": os.environ.get("S3_ENDPOINT_URL"),
        "config": Config(signature_version="s3v4"),
        "region_name": os.environ.get("S3_REGION_NAME"),
    }
    if os.environ.get("S3_ACCESS_KEY_ID"):
        params["aws_access_key_id"] = os.environ.get("S3_ACCESS_KEY_ID")
        params["aws_secret_access_key"] = os.environ.get("S3_SECRET_ACCESS_KEY")

    return boto3.client("s3", **params)

def _s_since_epoch(var_date_time):
    """ Convert datetime to seconds since the Unix epoch """
    return timegm(var_date_time.utctimetuple())


def to_datetime(s_since_epoch):
    """ Convert seconds since the Unix epoch to datetime """
    return datetime.fromtimestamp(s_since_epoch, tz=timezone.utc)


def to_iso8601(date):
    """ Return an ISO8601 formatted date """
    return date.isoformat()


def make_hash(password: str, salt: str = None) -> Tuple[str, str]:
    """Make a hash of a password.

    If a salt is not provided, a random one is created.

    Returns the hash and salt."""
    # NIST guidelines for password storage:
    #  * salt > 32 bits
    #  * PBKDF2
    #  * iterate at least 10,000 times.
    #  * TODO consider adding pepper (probably SECRET_KEY?)
    if salt is None:
        salt = secrets.token_urlsafe(32)
    return (
        hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 10000
        ).hex(),
        salt,
    )


def verify_hash(password: str, p_hash: str, salt: str) -> bool:
    """ Returns True when 'password' matches a value from make_hash(). """
    return make_hash(password, salt)[0] == p_hash


def make_jwt(user, max_expiration=None):
    """Create a JWT token for a user.

    Includes two non-jwt values:
     * uuid: a user uuid.
     * max-exp: the maximum date that we want to allow one to be able to refresh
                their JWT token (enforced by verify_jwt()). Formatted as seconds
                since the Unix epoch (same as exp field)
    """
    if max_expiration is None:
        max_expiration = datetime.now() + timedelta(days=JWT_MAX_EXPIRATION_DAYS)

    expiration = datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS)
    max_expiration = _s_since_epoch(max_expiration)
    return jwt.encode(
        {
            "uuid": user.uuid,
            "exp": expiration,
            "max-exp": max_expiration,
            "iss": current_app.name,
            "iat": datetime.utcnow(),
        },
        current_app.config["SECRET_KEY"],
        algorithm=JWT_ALGORITHM,
    )


def decode_jwt(jwt_string, secret=None):
    """Decode a JWT token.

    Returns the JWT if it is valid, otherwise None.
    """
    if secret is None:
        secret = current_app.config["SECRET_KEY"]

    try:
        a_jwt = jwt.decode(jwt_string, secret, algorithms=JWT_ALGORITHM)

        if "uuid" not in a_jwt or "max-exp" not in a_jwt:
            log("decode_jwt: missing uuid/max-exp", logging.WARN)
            return False

        return a_jwt
    except PyJWTError:
        return False


def verify_jwt(user, jwt_string, secret=None):
    """Verify that a JWT token is from a user, and is still valid.

    Returns True if the JWT is valid.
    """
    a_jwt = decode_jwt(jwt_string, secret)

    if not a_jwt:
        return False

    if int(a_jwt["max-exp"]) < _s_since_epoch(datetime.now()):
        return False

    return a_jwt["uuid"] == user.uuid


def log(message, level=logging.INFO):
    user_uuid = 0
    event = ""

    if has_request_context():
        event = request.path
        if "user" in g and g.user:
            user_uuid = g.user.uuid

    logger.log(level, message, extra={"user_uuid": user_uuid, "event": event})
