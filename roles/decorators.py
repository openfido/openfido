import logging
import re
from enum import Enum
from functools import wraps
from typing import List, TypeVar

from flask import g, request

from .queries import is_permitted

logger = logging.getLogger("roles")


PermissionOrPermissionList = TypeVar('PermissionOrPermissionList', int, List[int])

def make_permission_decorator(permissions_enum: Enum):
    """ Create a decorator that allows permissions defined by permissions_enum. """

    def permissions_required_decorator(permission: PermissionOrPermissionList):
        """ Decorator that ensures endpoint is called with an api_token with the
        required SystemPermission.code


        'permission' may be one permission code, or a list of permission codes.
        """

        required_permission = permissions_enum(permission)

        def decorator(view):
            @wraps(view)
            def wrapper(*args, **kwargs):
                if "Authorization" not in request.headers:
                    logger.warning("no authorization header")
                    return {}, 401
                if not request.headers["Authorization"].startswith("Bearer "):
                    logger.warning("authorization header not a bearer type")
                    return {}, 401

                matches = re.match(r"^Bearer (\S+)$", request.headers["Authorization"])
                if not matches:
                    logger.warning("invalid bearer token format")
                    return {}, 401

                g.api_key = matches.group(1)

                if not g.api_key:
                    logger.warning("unable to get api_key")
                    return {}, 401

                if not is_permitted(g.api_key, required_permission):
                    logger.warning(f"no permission found for {required_permission}")
                    return {}, 401

                return view(*args, **kwargs)

            return wrapper

        return decorator

    return permissions_required_decorator
