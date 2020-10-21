"""Users/autentication endpoints
"""
from functools import wraps
import re
import logging
import json

from flask import Blueprint, jsonify, request, g, send_file
from . import models, queries, services, utils
from .utils import BadRequestError
from werkzeug.exceptions import BadRequest

logging.basicConfig(level=logging.DEBUG)

auth_bp = Blueprint("auth", __name__)


def verify_system_admin(view):
    """Decorator to verify that a user has system admin privileges.

    Returns a 401 if the user is not a system admin.

    MUST CONTAIN g.user and g.jwt. This is added with `jwt_required` decorator.
    """

    @wraps(view)
    def wrapped(*args, **kwargs):
        g.is_system_admin = g.user.is_system_admin

        if not g.is_system_admin:
            utils.log("Admin access requested. User is not an Admin!", logging.WARN)
            return {}, 401

        return view(*args, **kwargs)

    return wrapped


def jwt_optional(view):
    """Decorator to check for an optional but valid JWT token to access an endpoint.

    Adds g.user and g.jwt on success.
    """

    @wraps(view)
    def wrapper(*args, **kwargs):
        if "Authorization" in request.headers and request.headers[
            "Authorization"
        ].startswith("Bearer "):
            matches = re.match(r"^Bearer (\S+)$", request.headers["Authorization"])
            if matches:
                g.jwt = utils.decode_jwt(matches.group(1))
                if g.jwt:
                    g.user = queries.find_user_by_uuid(g.jwt["uuid"])

                if not g.user:
                    utils.log("no such user", logging.WARN)
                    return {}, 401

                if not utils.verify_jwt(g.user, matches.group(1)):
                    utils.log("invalid JWT token", logging.WARN)
                    return {}, 401

        return view(*args, **kwargs)

    return wrapper


def jwt_required(view):
    """Decorator to require a valid JWT token to access an endpoint.

    Adds g.user and g.jwt on success.
    """

    @wraps(view)
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            utils.log("no authorization header", logging.WARN)
            return {}, 401
        if not request.headers["Authorization"].startswith("Bearer "):
            utils.log("authorization header not a bearer type", logging.WARN)
            return {}, 401

        matches = re.match(r"^Bearer (\S+)$", request.headers["Authorization"])
        if not matches:
            utils.log("invalid bearer token format", logging.WARN)
            return {}, 401

        g.jwt = utils.decode_jwt(matches.group(1))
        if not g.jwt:
            utils.log("unable to decode JWT", logging.WARN)
            return {}, 401

        g.user = queries.find_user_by_uuid(g.jwt["uuid"])
        if not g.user:
            utils.log("no such user", logging.WARN)
            return {}, 401

        if not utils.verify_jwt(g.user, matches.group(1)):
            utils.log("invalid JWT token", logging.WARN)
            return {}, 401

        services.update_user_last_active_at(g.user)
        return view(*args, **kwargs)

    return wrapper


def verify_content_type_and_params(required_keys, optional_keys):
    """ Decorator enforcing content type and body keys in an endpoint. """

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            def validate(item):
                request_keys = set(item.keys())
                required_set = set(required_keys)
                optional_set = set(optional_keys)
                if not required_set <= request_keys:
                    utils.log(
                        f"invalid payload keys {list(item.keys())}",
                        logging.WARN,
                    )
                    return False
                if len(request_keys - required_set.union(optional_set)) > 0:
                    utils.log("unknown key passed to request", logging.WARN)
                    return False
                return True

            if request.headers.get("Content-Type", None) != "application/json":
                utils.log("invalid content type", logging.WARN)
                return {}, 400

            try:
                if not validate(request.json):
                    utils.log("invalid object", logging.WARN)
                    return {}, 400
                return view(*args, **kwargs)
            except BadRequest as bad_request:
                utils.log("Unable to decode JSON", logging.WARN)
                return {}, 400

            utils.log("unknown data passed to request", logging.WARN)
            return {}, 400

        return wrapper

    return decorator


@auth_bp.route("", methods=["POST"])
@jwt_optional
@verify_content_type_and_params(
    ["email", "password", "first_name", "last_name"],
    ["invitation_token"],
)
def create_user():
    """Create a user.
    ---
    securitySchemes:
      bearerAuth:
        type: http
        scheme: bearer
        bearerFormat: JWT
    security:
      - bearerAuth: []
    requestBody:
      description: "An email, password, and name of user."
      required: true
      content:
        application/json:
          schema:
            type: "object"
            required:
              - email
              - password
              - first_name
              - last_name
            properties:
              email:
                type: "string"
                format: email
              password:
                type: "string"
              first_name:
                type: "string"
              last_name:
                type: "string"
              invitation_token:
                type: "string"
                format: uuid
    responses:
      "200":
        description: "Created"
        content:
          application/json:
            schema:
              type: object
              properties:
                uuid:
                  type: string
                email:
                  type: string
                  format: email
                token:
                  type: string
                  format: JWT
      "400":
        description: "Bad request"
      "401":
        description: "Invalid input"
    """
    email = request.json["email"]
    password = request.json["password"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]

    invitation = None
    if "invitation_token" in request.json:
        invitation_token = request.json["invitation_token"]
        invitation = queries.find_invitation_by_invitation_token(invitation_token)

        if invitation is None:
            utils.log("create: invalid invitation token", logging.WARN)
            return {"message": "invalid invitation token"}, 400

        if not invitation.email_address == email:
            utils.log("create: incorrect email address", logging.WARN)
            return {"message": "incorrect email address"}, 400

    if invitation is None and not (hasattr(g, "user") and g.user.is_system_admin):
        utils.log("create: not authorized", logging.WARN)
        return {}, 401

    if queries.find_user_by_email(email):
        utils.log("create: user exists", logging.WARN)
        return {"message": "user already exists"}, 400

    try:
        user = services.create_user(email, password, first_name, last_name)
        if invitation:
            services.accept_invitation(invitation.invitation_token)
        models.db.session.commit()

        utils.log("user created")

        return user.serialize()
    except BadRequestError as bad_request_error:
        utils.log(f"could not create user: {bad_request_error}", logging.WARN)
        return {"message": str(bad_request_error)}, 400


@auth_bp.route("/<request_uuid>/profile", methods=["PUT"])
@verify_content_type_and_params(["email", "first_name", "last_name"], [])
@jwt_required
def update_user(request_uuid):
    """Update a user by uuid"""
    user = queries.find_user_by_uuid(request_uuid)

    if not user:
        utils.log("A user requested a profile, but was not an admin", logging.WARN)
        return {}, 401

    if g.user != user:
        utils.log("ERROR: Cannot update a different user's profile")
        return {}, 401

    email = request.json["email"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]

    try:
        user = services.update_user(user, email, first_name, last_name)
        return user.serialize()

    except BadRequestError as bad_request_error:
        utils.log(f"could not update user: {bad_request_error}", logging.WARN)
        return {"message": str(bad_request_error)}, 400


@auth_bp.route("/<user_uuid>/profile", methods=["GET"])
@jwt_required
def get_user_profile(user_uuid):
    """Get a user's profile information.
    ---

    requestBody:
      description: "Get the profile for the specified user."
      required: true
      content:
        application/json:
          schema:
            type: "object"
            required:
              - uuid
            properties:
              uuid:
                type: "string"
                format: uuid
    responses:
      "200":
        description: "Described"
        content:
          application/json:
            schema:
              type: object
              properties:
                uuid:
                  type: string
                  format: uuid
                email:
                  type: string
                  format: email
                first_name:
                  type: string
                last_name:
                  type: string
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
      "400":
        description: "Bad request"
      "401":
        description: "Invalid input"
    """
    if g.user.uuid != user_uuid:
        utils.log("Invalid user", logging.WARN)
        return {}, 401

    return g.user.serialize()


@auth_bp.route("/<user_uuid>/avatar", methods=["PUT"])
@jwt_required
def update_user_avatar(user_uuid):
    """Update a user's avatar image.
    ---
    requestBody:
      description: "binary file content"
      required: true
    responses:
      "200":
        description: "Updated"
      "400":
        description: "Bad request"
      "413":
        description: "Payload Too Large"
    """
    user = queries.find_user_by_uuid(user_uuid)

    if not user:
        utils.log("Invalid user", logging.WARN)
        return {}, 401

    if g.user != user:
        utils.log("ERROR: Cannot update a different user's avatar")
        return {}, 401

    try:
        services.update_user_avatar(user, request.stream)
        return {}, 200

    except BadRequestError as bad_request_error:
        utils.log(f"could not update user avatar: {bad_request_error}", logging.WARN)
        return {"message": str(bad_request_error)}, 400


@auth_bp.route("/<user_uuid>/avatar", methods=["GET"])
@jwt_required
def get_user_avatar(user_uuid):
    """Get a user's avatar image.
    ---
    requestBody:
    responses:
      "200":
        description: "Found"
      "400":
        description: "Bad request"
    """
    user = queries.find_user_by_uuid(user_uuid)

    if not user:
        utils.log("Invalid user", logging.WARN)
        return {}, 401

    try:
        stream = services.get_user_avatar(user)
        return send_file(stream, attachment_filename="avatar.png")
    except BadRequestError as bad_request_error:
        utils.log(f"could not get user avatar: {bad_request_error}", logging.WARN)
        return {"message": str(bad_request_error)}, 400


@auth_bp.route("/<user_uuid>/organizations", methods=["GET"])
@jwt_required
def get_user_organizations(user_uuid):
    """Get a user's profile information.
    ---

    requestBody:
      description: "Get a user's organizations."
      required: true
      content:
        application/json:
          schema:
            type: "object"
            required:
              - uuid
            properties:
              uuid:
                type: "string"
                format: uuid
    responses:
      "200":
        description: "Described"
        content:
          application/json:
            schema:
              type: object
              properties:
                organizations:
                  type: array
      "400":
        description: "Bad request"
      "401":
        description: "Invalid input"
    """

    if g.user.uuid != user_uuid:
        utils.log("Invalid user", logging.WARN)
        return {}, 401

    memberships = queries.find_user_organization_memberships(g.user)
    return jsonify([m.serialize_organization_role() for m in memberships])


@auth_bp.route("/auth", methods=["POST"])
@verify_content_type_and_params(["email", "password"], [])
def auth_user():
    """Authenticate a user.
    ---

    requestBody:
      description: "An email and password."
      required: true
      content:
        application/json:
          schema:
            type: "object"
            required:
              - email
              - password
            properties:
              email:
                type: "string"
                format: email
              password:
                type: "string"
    responses:
      "200":
        description: "Created"
        content:
          application/json:
            schema:
              type: object
              properties:
                uuid:
                  type: string
                email:
                  type: string
                  format: email
                token:
                  type: string
                  format: JWT
      "400":
        description: "Bad request"
      "401":
        description: "Invalid input"
    """
    email = request.json["email"]
    password = request.json["password"]
    user = queries.find_user_by_email(email)
    if user is None:
        utils.log("user does not exist", logging.WARN)
        return {}, 401

    if not utils.verify_hash(password, user.password_hash, user.password_salt):
        utils.log("verify hash failed", logging.WARN)
        return {}, 401

    utils.log("authorized user")
    response = user.serialize()
    response["token"] = token = utils.make_jwt(user).decode("utf-8")
    return response


@auth_bp.route("/auth/refresh", methods=["POST"])
@jwt_required
def refresh():
    """Refresh a JWT token.
    ---
    securitySchemes:
      bearerAuth:
        type: http
        scheme: bearer
        bearerFormat: JWT
    security:
      - bearerAuth: []
    responses:
      "200":
        description: "Created"
        content:
          application/json:
            schema:
              type: object
              properties:
                token:
                  type: string
                  format: JWT
      "400":
        description: "Bad request"
      "401":
        description: "Invalid input"
    """
    if request.headers.get("Content-Type", None) != "application/json":
        utils.log("invalid content type", logging.WARN)
        return {"message": "invalid content type"}, 400

    utils.log("token refreshed")
    return jsonify(
        token=utils.make_jwt(g.user, utils.to_datetime(g.jwt["max-exp"])).decode(
            "utf-8"
        )
    )


@auth_bp.route("/password", methods=["PUT"])
@verify_content_type_and_params(["old_password", "new_password"], [])
@jwt_required
def change_password():
    """Allow a user to change their password.
    requestBody:
      description: "The new password."
      required: true
      content:
        application/json:
          schema:
            type: "object"
            required:
              - old_password
              - new_password
            properties:
              old_password:
                type: "string"
              new_password:
                type: "string"
    responses:
      "200":
        description: "Updated"
      "400":
        description: "Bad request"
    """
    old_password = request.json["old_password"]
    new_password = request.json["new_password"]

    try:
        services.change_password(g.user, old_password, new_password)
        utils.log("change_password: updated password")
        return {}, 200
    except BadRequestError as bad_request_error:
        utils.log(bad_request_error, logging.ERROR)
        return {}, 401


@auth_bp.route("/request_password_reset", methods=["POST"])
@verify_content_type_and_params(["email"], [])
def reset():
    """Send user a password reset email.
    ---

    requestBody:
      description: "An email."
      required: true
      content:
        application/json:
          schema:
            type: "object"
            required:
              - email
            properties:
              email:
                type: "string"
                format: email
    responses:
      "200":
        description: "Created"
      "400":
        description: "Bad request"
    """
    email = request.json["email"]
    user = queries.find_user_by_email(email)
    if not user:
        return {}, 200

    if not services.request_password_reset(user):
        utils.log("reset: unable to send request_password_reset", logging.WARN)
        return {"message": "unable to send password reset"}, 400

    utils.log("reset_token sent")
    return {}, 200


@auth_bp.route("/reset_password", methods=["PUT"])
@verify_content_type_and_params(["reset_token", "password"], [])
def reset_password():
    """Reset a user's password.
    requestBody:
      description: "A new password, and reset_token."
      required: true
      content:
        application/json:
          schema:
            type: "object"
            required:
              - password
              - reset_token
            properties:
              password:
                type: "string"
              reset_token:
                type: "string"
    responses:
      "200":
        description: "Updated"
      "400":
        description: "Bad request"
    """

    password = request.json["password"]
    reset_token = request.json["reset_token"]
    user = queries.find_user_by_reset_token(reset_token)

    if not user:
        utils.log("reset_password: user does not exist", logging.WARN)
        return {"message": "invalid reset token"}, 400

    try:
        services.reset_password(user, password, reset_token)
        utils.log("reset_password: updated password")
        return {}, 200
    except BadRequestError as bad_request_error:
        utils.log(f"could not reset password: {bad_request_error}", logging.WARN)
        return {"message": str(bad_request_error)}, 400


@auth_bp.errorhandler(500)
def handle_error(exception):
    """Handles errors and returns 500"""
    utils.log(f"unspecified error: {exception}")
    return {}, 500
