import logging
import re
from enum import IntEnum, unique
from functools import wraps
from jwt.exceptions import DecodeError

import jwt
from application_roles.decorators import make_permission_decorator
from flask import g, request

from .services import fetch_is_user_in_org

logger = logging.getLogger("utils")


@unique
class ApplicationsEnum(IntEnum):
    """ All possible types of applications that can access this API. """

    REACT_CLIENT = 1


permissions_required = make_permission_decorator(ApplicationsEnum)
any_application_required = permissions_required(list(ApplicationsEnum))


def validate_organization():
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
            if request.headers.get("Content-Type", None) != "application/json":
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
                    return {"message": "Unable to find organization by uuid provided"}, 404

                return view(*args, **kwargs)
            except DecodeError:
                logger.warning("unable to decode JWT")
                return {}, 401


        return wrapper

    return decorator
