import logging
from functools import wraps

from flask import request, current_app

import boto3
from botocore.client import Config
from roles.decorators import make_permission_decorator
from .model_utils import SystemPermissionEnum
from .constants import (
    S3_ACCESS_KEY_ID,
    S3_SECRET_ACCESS_KEY,
    S3_ENDPOINT_URL,
    S3_REGION_NAME,
)

logger = logging.getLogger("utils")

permissions_required = make_permission_decorator(SystemPermissionEnum)


def get_s3():
    return boto3.client(
        "s3",
        endpoint_url=current_app.config[S3_ENDPOINT_URL],
        aws_access_key_id=current_app.config[S3_ACCESS_KEY_ID],
        aws_secret_access_key=current_app.config[S3_SECRET_ACCESS_KEY],
        config=Config(signature_version="s3v4"),
        region_name=current_app.config[S3_REGION_NAME],
    )


def to_iso8601(date):
    """ Return an ISO8601 formatted date """
    return date.isoformat()


def verify_content_type_and_params(required_keys, optional_keys):
    """ Decorator enforcing content type and body keys in an endpoint. """

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if request.headers.get("Content-Type", None) != "application/json":
                logger.warning("invalid content type")
                return {}, 400

            required_set = set(required_keys)
            optional_set = set(optional_keys)
            if len(required_set) == len(optional_set) == 0:
                return view(*args, **kwargs)

            request_keys = set(request.json.keys())
            if not required_set <= request_keys:
                logger.warning(
                    f"create: invalid payload keys {list(request.json.keys())}, requires {required_keys}",
                )
                return {}, 400
            if len(request_keys - required_set.union(optional_set)) > 0:
                logger.warning("unknown key passed to request")
                return {}, 400

            return view(*args, **kwargs)

        return wrapper

    return decorator
