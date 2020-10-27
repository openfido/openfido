import logging
from functools import wraps

from flask import request, current_app

from application_roles.decorators import make_permission_decorator
from .model_utils import SystemPermissionEnum

logger = logging.getLogger("utils")

permissions_required = make_permission_decorator(SystemPermissionEnum)


def to_iso8601(date):
    """ Return an ISO8601 formatted date """
    return date.isoformat()


def verify_content_type():
    """ Decorator enforcing application/json content type """

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if request.headers.get("Content-Type", None) != "application/json":
                logger.warning("invalid content type")
                return {"message": "application/json content-type is required."}, 400

            return view(*args, **kwargs)

        return wrapper

    return decorator


def verify_content_type_and_params(required_keys, optional_keys):
    """ Decorator enforcing content type and body keys in an endpoint. """

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if request.headers.get("Content-Type", None) != "application/json":
                logger.warning("invalid content type")
                return {"message": "application/json content-type is required."}, 400

            required_set = set(required_keys)
            optional_set = set(optional_keys)
            if len(required_set) == len(optional_set) == 0:
                return view(*args, **kwargs)

            request_keys = set(request.json.keys())
            if not required_set <= request_keys:
                message = (
                    f"create: invalid payload keys {list(request.json.keys())}, "
                    + f"requires {required_keys}",
                )
                logger.warning(message)
                return {"message": message}, 400
            if len(request_keys - required_set.union(optional_set)) > 0:
                message = "unknown key passed to request"
                logger.warning(message)
                return {"message": message}, 400

            return view(*args, **kwargs)

        return wrapper

    return decorator
