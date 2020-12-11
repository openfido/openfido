import logging
from enum import Enum
from functools import wraps

from flask import g, request

from .queries import is_permitted

logger = logging.getLogger("application_roles")

ROLES_KEY = "Workflow-API-Key"


def make_permission_decorator(permissions_enum):
    """ Create a decorator that allows permissions defined by permissions_enum. """

    def permissions_required_decorator(permissions):
        """Decorator that ensures endpoint is called with an api_token that is
        associated with the required list of SystemPermission values.
        """

        def decorator(view):
            @wraps(view)
            def wrapper(*args, **kwargs):
                if ROLES_KEY not in request.headers:
                    message = "no authorization header"
                    logger.warning(message)
                    return {"message": message}, 401

                g.api_key = request.headers[ROLES_KEY]

                for permission in permissions:
                    required_permission = permissions_enum(permission)

                    if not is_permitted(g.api_key, required_permission):
                        message = f"no permission found for {required_permission.name}"
                        logger.warning(message)
                        return {"message": message}, 401

                return view(*args, **kwargs)

            return wrapper

        return decorator

    return permissions_required_decorator
