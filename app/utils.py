import hashlib
import logging
import re
import secrets
from enum import IntEnum, unique
from functools import wraps

import jwt
import secrets
from application_roles.decorators import make_permission_decorator
from flask import g, request
from jwt.exceptions import DecodeError
from requests import HTTPError
from simplejson.errors import JSONDecodeError

from .services import fetch_is_user_in_org

logger = logging.getLogger("utils")


@unique
class ApplicationsEnum(IntEnum):
    """ All possible types of applications that can access this API. """

    REACT_CLIENT = 1


permissions_required = make_permission_decorator(ApplicationsEnum)
any_application_required = permissions_required(list(ApplicationsEnum))


def validate_organization(requires_json=True):
    """Decorator enforcing that organization_uuid is valid, and that the
    content type is application/json.

    Note: assumes that the method called has <organization_uuid> as the first
    argument in its route pattern, and is the first parameter.

    Assigns g.organization_uuid to the organization uuid
    Assigns g.jwt_token on success to JWT token.
    Assigns g.user_uuid on success to user's uuid decoded from JWT token.
    """

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if (
                requires_json
                and request.headers.get("Content-Type", None) != "application/json"
            ):
                logger.warning("invalid content type")
                return {"message": "application/json content-type is required."}, 400

            if "Authorization" not in request.headers:
                logger.warning("No Authorization header supplied")
                return {}, 401

            matches = re.match(r"^Bearer (\S+)$", request.headers["Authorization"])
            if not matches:
                logger.warning("invalid bearer token format")
                return {}, 401

            g.jwt_token = matches.group(1)
            try:
                decoded_token = jwt.decode(g.jwt_token, verify=False)

                g.user_uuid = decoded_token["uuid"]
                g.organization_uuid = kwargs["organization_uuid"]

                if not fetch_is_user_in_org(
                    kwargs["organization_uuid"], g.jwt_token, g.user_uuid
                ):
                    logger.warning("Could not find organization")
                    return {
                        "message": "Unable to find organization by uuid provided"
                    }, 404

                return view(*args, **kwargs)
            except HTTPError:
                logger.warning("Failing to access auth server")
                return {}, 503
            except DecodeError:
                logger.warning("unable to decode JWT")
                return {}, 401
            except JSONDecodeError:
                logger.warning("Unable to read auth server response")
                return {}, 401

        return wrapper

    return decorator

def make_hash(password, salt=None):
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


def verify_hash(password, p_hash, salt):
    """ Returns True when 'password' matches a value from make_hash(). """
    return make_hash(password, salt)[0] == p_hash
