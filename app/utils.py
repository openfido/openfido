import logging
from functools import wraps

from flask import request

import boto3
from botocore.client import Config
from roles.decorators import make_permission_decorator
from .model_utils import SystemPermissionEnum

logger = logging.getLogger("utils")

permissions_required = make_permission_decorator(SystemPermissionEnum)


# TODO make this configurable
s3 = boto3.client(
    "s3",
    endpoint_url="http://storage:9000",
    aws_access_key_id="AKIAIOSFODNN7EXAMPLE",
    aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
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
