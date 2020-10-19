"""Organization endpoints
"""
import logging

from flask import Blueprint, jsonify, request, g
from . import models, queries, services, utils
from .utils import BadRequestError
from .auth import verify_system_admin, jwt_required, verify_content_type_and_params

logging.basicConfig(level=logging.DEBUG)

org_bp = Blueprint("org", __name__)


@org_bp.route("", methods=["POST"])
# requires a jwt token for an active user
@jwt_required
@verify_system_admin
@verify_content_type_and_params(["name"], [])
def create_organization():
    """Create an organization.
    ---
    securitySchemes:
        bearerAuth:
            type: http
            scheme: bearer
            bearerFormat: JWT
    security:
        - bearerAuth: []
    requestBody:
        description: "A name for the organization."
        required: true
        content:
            application/json:
                schema:
                    type: "object"
                    required:
                        - name
                    properties:
                        name:
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
                            name:
                                type: string
        "400":
            description: "Bad request"
        "401":
            description: "Invalid input"
    """

    try:
        name = request.json["name"]
        organization = services.create_organization(name, g.user)
        return organization.serialize()
    except BadRequestError as bad_request_error:
        utils.log(f"could not create organization: {bad_request_error}", logging.WARN)
        return {"message": str(bad_request_error)}, 400


@org_bp.route("<organization_uuid>", methods=["DELETE"])
@jwt_required
@verify_system_admin
def delete_organization(organization_uuid):
    """Delete an organization.
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
                    description: "Deleted"
            "400":
                    description: "Bad request"
            "401":
                    description: "Invalid input"
    """
    organization = queries.find_organization_by_uuid(organization_uuid)
    if not organization:
        utils.log("delete: org does not exist", logging.WARN)
        return {"message": "invalid organization"}, 400
    try:
        services.delete_organization(organization)

        utils.log("organization deleted")

        return {}, 200
    except BadRequestError as bad_request_error:
        utils.log(f"could not delete organization: {bad_request_error}", logging.WARN)
        return {"message": str(bad_request_error)}, 400


@org_bp.route("<organization_uuid>/profile", methods=["PUT"])
# requires a jwt token for an active user
@verify_content_type_and_params(["name"], [])
@jwt_required
def update_organization_profile(organization_uuid):
    """Update an organization profile.
    ---
    securitySchemes:
        bearerAuth:
            type: http
            scheme: bearer
            bearerFormat: JWT
    security:
        - bearerAuth: []
    requestBody:
        description: "A name for the organization."
        required: true
        content:
            application/json:
                schema:
                    type: "object"
                    required:
                        - name
                    properties:
                        name:
                            type: "string"
    responses:
        "200":
            description: "Updated"
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            uuid:
                                type: string
                            name:
                                type: string
        "400":
            description: "Bad request"
        "401":
            description: "Invalid input"
    """
    name = request.json["name"]
    organization = queries.find_organization_by_uuid(organization_uuid)

    if not organization:
        utils.log("could not update organization: invalid organization_uuid")
        return {"message": "invalid organization"}, 400

    if not queries.is_user_organization_admin(organization, g.user):
        utils.log("could not update organization: not an organization admin")
        return {}, 401

    try:
        organization = services.update_organization(organization, name)
        g.organization = organization

        utils.log("organization updated")

        return organization.serialize()
    except BadRequestError as bad_request_error:
        utils.log(f"could not update organization: {bad_request_error}", logging.WARN)
        return {"message": str(bad_request_error)}, 400


@org_bp.route("/<organization_uuid>/logo", methods=["PUT"])
@jwt_required
def update_organization_logo(organization_uuid):
    """Update an organization's logo image.
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
    organization = queries.find_organization_by_uuid(organization_uuid)

    if not organization:
        utils.log("Invalid organization", logging.WARN)
        return {}, 401

    if not queries.is_user_organization_admin(organization, g.user):
        utils.log("ERROR: User is not an organization admin")
        return {}, 401

    try:
        services.update_organization_logo(organization, request.stream)
        return {}, 200
    except BadRequestError as bad_request_error:
        utils.log(
            f"could not update organization logo: {bad_request_error}", logging.WARN
        )
        return {"message": str(bad_request_error)}, 400


@org_bp.route("/<organization_uuid>/logo", methods=["GET"])
@jwt_required
def get_organization_logo(organization_uuid):
    """Get an organization's logo image.
    ---
    requestBody:
    responses:
      "200":
        description: "Found"
      "400":
        description: "Bad request"
    """
    organization = queries.find_organization_by_uuid(organization_uuid)

    if not organization:
        utils.log("Invalid organization", logging.WARN)
        return {}, 401

    try:
        stream = services.get_organization_logo(organization)
        return send_file(stream)
    except BadRequestError as bad_request_error:
        utils.log(f"could not get organization logo: {bad_request_error}", logging.WARN)
        return {"message": str(bad_request_error)}, 400


@org_bp.route("/<organization_uuid>/profile", methods=["GET"])
@jwt_required
def get_organization_profile(organization_uuid):
    """Get an organization's profile information.
    ---

    requestBody:
        description: "Get the profile for the specified org."
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
                            name:
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

    if not queries.find_organization_by_uuid(organization_uuid):
        utils.log("an organization was requested, but doesn't exist", logging.WARN)
        return {"message": "invalid organization"}, 400

    organization = queries.find_organization_by_uuid(organization_uuid)
    if not queries.find_organization_member_role(organization, g.user):
        utils.log("user is not a member for selected organization", logging.WARN)
        return {}, 401

    return organization.serialize()


@org_bp.route("/<organization_uuid>/members", methods=["GET"])
@jwt_required
def get_organization_members(organization_uuid):
    """Get an organization's members.
    ---

    requestBody:
        description: "Get the members for the specified org."
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
                        items:
                        $id: '#/items'
                        anyOf:
                        -   $id: '#/items/anyOf/0'
                            additionalProperties: true
                            default: {}
                            description: get members for the organization.
                            examples:
                            -   created_at: Tue, 15 Sep 2020 00:00:00 GMT
                            email: admin@email.com
                            first_name: John
                            is_system_admin: true
                            last_name: Smith
                            updated_at: Tue, 15 Sep 2020 00:00:00 GMT
                            uuid: ded3f053-d25e-4873-8e38-7fbf9c38
                            properties:
                            created_at:
                                $id: '#/items/anyOf/0/properties/created_at'
                                default: ''
                                examples:
                                - Tue, 15 Sep 2020 00:00:00 GMT
                                title: The created_at schema
                                type: string
                            email:
                                $id: '#/items/anyOf/0/properties/email'
                                default: ''
                                examples:
                                - admin@email.com
                                title: The email schema
                                type: string
                            first_name:
                                $id: '#/items/anyOf/0/properties/first_name'
                                default: ''
                                examples:
                                - John
                                title: The first_name schema
                                type: string
                            is_system_admin:
                                $id: '#/items/anyOf/0/properties/is_system_admin'
                                default: false
                                examples:
                                - true
                                title: The is_system_admin schema
                                type: boolean
                            last_name:
                                $id: '#/items/anyOf/0/properties/last_name'
                                default: ''
                                examples:
                                - Smith
                                title: The last_name schema
                                type: string
                            updated_at:
                                $id: '#/items/anyOf/0/properties/updated_at'
                                default: ''
                                examples:
                                - Tue, 15 Sep 2020 00:00:00 GMT
                                title: The updated_at schema
                                type: string
                            uuid:
                                $id: '#/items/anyOf/0/properties/uuid'
                                default: ''
                                examples:
                                - ded3f053-d25e-4873-8e38-7fbf9c38
                                title: The uuid schema
                                type: string
                            required:
                            - created_at
                            - email
                            - first_name
                            - is_system_admin
                            - last_name
                            - updated_at
                            - uuid
                            title: The first anyOf schema
                            type: object
                        title: The root schema
                        type: array
        "400":
            description: "Bad request"
        "401":
            description: "Invalid input"
    """

    organization = queries.find_organization_by_uuid(organization_uuid)
    if not organization:
        utils.log("an organization was requested, but doesn't exist", logging.WARN)
        return {"message": "invalid organization"}, 400

    if not queries.is_user_organization_admin(organization, g.user):
        utils.log("user is not admin for selected organization", logging.WARN)
        return {}, 401

    organization = queries.find_organization_by_uuid(organization_uuid)
    members = queries.find_organization_members(organization)

    return jsonify([m.serialize_user_role() for m in members])


@org_bp.route("/<organization_uuid>/invitations", methods=["POST"])
@jwt_required
@verify_content_type_and_params(["email"], [])
def invite_organization_member(organization_uuid):
    """Create an invitation to an organization for a user by email.
    ---
    securitySchemes:
        bearerAuth:
            type: http
            scheme: bearer
            bearerFormat: JWT
    security:
        - bearerAuth: []
    requestBody:
        description: "A name for the organization."
        required: true
        content:
            application/json:
                schema:
                    type: "object"
                    required:
                        - name
                    properties:
                        name:
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
        "400":
            description: "Bad request"
        "401":
            description: "Invalid input"
    """
    email = request.json["email"]
    # write a query to find org by name, then return a bad request if it returns true

    organization = queries.find_organization_by_uuid(organization_uuid)
    if not organization:
        utils.log("an organization was requested, but doesn't exist", logging.WARN)
        return {"message": "invalid organization"}, 400

    if not queries.is_user_organization_admin(organization, g.user):
        utils.log("create: user is not admin for selected organization", logging.WARN)
        return {}, 401

    user = queries.find_user_by_email(email)
    if user and queries.find_organization_member_role(organization, user):
        utils.log("invited user is already a member", logging.WARN)
        return {"message": "invited user is already a member"}, 400

    try:
        invitation = services.create_invitation(organization, email)
        models.db.session.commit()
        return {}, 200
    except BadRequestError as bad_request_error:
        utils.log(
            f"could not invite organization member: {bad_request_error}", logging.WARN
        )
        return {"message": str(bad_request_error)}, 400


@org_bp.route("/<organization_uuid>/invitations", methods=["GET"])
@jwt_required
def list_organization_invitations(organization_uuid):
    """Get a list of all outstanding invitations for this Organization
    ---
    responses:
        "200":
            description: "Described"
        "400":
            description: "Bad request"
        "401":
            description: "Invalid input"
    """

    organization = queries.find_organization_by_uuid(organization_uuid)
    if not organization:
        utils.log("an organization was requested, but doesn't exist", logging.WARN)
        return {"message": "invalid organization"}, 400

    if not queries.is_user_organization_admin(organization, g.user):
        utils.log("user is not admin for selected organization", logging.WARN)
        return {}, 401

    invitations = queries.find_pending_invitations_by_organization(organization)

    return jsonify([invite.serialize() for invite in invitations])


@org_bp.route("/invitations/accept", methods=["POST"])
@verify_content_type_and_params(["invitation_token"], [])
def accept_organization_invitation():
    """Accept an invitation to join an organization.
    ---

    requestBody:
        description: "Invitation Token"
        required: true
        content:
            application/json:
                schema:
                    type: "object"
                    required:
                        - invitation_token
                    properties:
                        invitation_token:
                            type: "string"
                            format: uuid
    responses:
        "200":
            description: "Updated"
        "400":
            description: "Bad request"
        "401":
            description: "Invalid input"
    """

    try:
        invitation_token = request.json["invitation_token"]
        invitation = queries.find_invitation_by_invitation_token(invitation_token)
        services.accept_invitation(invitation_token)
        return {"organization_uuid": invitation.organization.uuid}, 200
    except BadRequestError as bad_request_error:
        utils.log(f"could not accept invitation: {bad_request_error}", logging.WARN)
        return {"message": str(bad_request_error)}, 400


@org_bp.route("/invitations/reject", methods=["POST"])
@verify_content_type_and_params(["invitation_token"], [])
def reject_organization_invitation():
    """Accept an invitation to join an organization.
    ---

    requestBody:
        description: "Invitation Token"
        required: true
        content:
            application/json:
                schema:
                    type: "object"
                    required:
                        - invitation_token
                    properties:
                        invitation_token:
                            type: "string"
                            format: uuid
    responses:
        "200":
            description: "Updated"
        "400":
            description: "Bad request"
        "401":
            description: "Invalid input"
    """

    try:
        invitation_token = request.json["invitation_token"]
        services.reject_invitation(invitation_token)
        return {}, 200
    except BadRequestError as bad_request_error:
        utils.log(f"could not reject invitation: {bad_request_error}", logging.WARN)
        return {"message": str(bad_request_error)}, 400


@org_bp.route("/invitations/cancel", methods=["POST"])
@jwt_required
@verify_content_type_and_params(["invitation_uuid"], [])
def cancel_organization_invitation():
    """Accept an invitation to join an organization.
    ---

    requestBody:
        description: "Invitation Token"
        required: true
        content:
            application/json:
                schema:
                    type: "object"
                    required:
                        - invitation_token
                    properties:
                        invitation_token:
                            type: "string"
                            format: uuid
    responses:
        "200":
            description: "Updated"
        "400":
            description: "Bad request"
        "401":
            description: "Invalid input"
    """

    invitation_uuid = request.json["invitation_uuid"]
    invitation = queries.find_invitation_by_invitation_uuid(invitation_uuid)

    if invitation is None:
        utils.log("cancel_organization_invitation: invitation is invalid", logging.WARN)
        return {"message": "invalid invitation"}, 400

    organization = queries.find_organization_by_id(invitation.organization_id)
    if not queries.is_user_organization_admin(organization, g.user):
        utils.log(
            "cancel_organization_invitation: user is not admin for selected organization",
            logging.WARN,
        )
        return {}, 401

    try:
        services.cancel_invitation(invitation_uuid)
        return {}, 200
    except BadRequestError as bad_request_error:
        utils.log(f"could not cancel invitation: {bad_request_error}", logging.WARN)
        return {"message": str(bad_request_error)}, 400


@org_bp.route("/<organization_uuid>/members/<user_uuid>/role", methods=["PUT"])
@jwt_required
@verify_content_type_and_params(["role"], [])
def change_organization_member_role(organization_uuid, user_uuid):
    """Change a member's role in an organization.
    ---

    requestBody:
        description: "Get the members for the specified org."
        required: true
        content:
            application/json:
                schema:
                    type: "object"
                    required:
                        - role
                    properties:
                        role:
                            type: "string"
    responses:
        "200":
            description: "Updated"
        "400":
            description: "Bad request"
        "401":
            description: "Invalid input"
    """

    organization = queries.find_organization_by_uuid(organization_uuid)
    if not organization:
        utils.log("an organization was requested, but doesn't exist", logging.WARN)
        return {"message": "invalid organization"}, 400

    if not queries.is_user_organization_admin(organization, g.user):
        utils.log("could not update organization: not an organization admin")
        return {}, 401

    try:
        role = request.json["role"]
        user = queries.find_user_by_uuid(user_uuid)
        services.update_organization_member_role(organization, user, role)
        return {}, 200
    except BadRequestError as bad_request_error:
        utils.log(
            f"could not update organization member role: {bad_request_error}",
            logging.WARN,
        )
        return {"message": str(bad_request_error)}, 400


@org_bp.route("/<organization_uuid>/members/<user_uuid>", methods=["DELETE"])
@jwt_required
def remove_organization_member(organization_uuid, user_uuid):
    """Delete a member from an organization.
    ---

    requestBody:
        description: "Get the members for the specified org."
        required: true
        content:
            application/json:
                schema:
                    type: "object"
    responses:
        "200":
            description: "Member was successfully removed from Organization."
        "400":
            description: "Bad request"
        "401":
            description: "Invalid input"
    """

    organization = queries.find_organization_by_uuid(organization_uuid)
    if not organization:
        utils.log("an organization was requested, but doesn't exist", logging.WARN)
        return {"message": "invalid organization"}, 400

    if not queries.is_user_organization_admin(organization, g.user):
        utils.log("could not update organization: not an organization admin")
        return {}, 401

    user = queries.find_user_by_uuid(user_uuid)
    if not user:
        utils.log("a user was requested, but doesn't exist", logging.WARN)
        return {"message": "invalid user"}, 400

    try:
        services.remove_organization_member(organization, user)
        return {}, 200
    except BadRequestError as bad_request_error:
        utils.log(
            f"could not remove organization member: {bad_request_error}", logging.WARN
        )
        return {"message": str(bad_request_error)}, 400
