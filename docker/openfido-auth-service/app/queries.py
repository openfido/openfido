import uuid
from .utils import BadRequestError
from .models import (
    ROLE_ADMINISTRATOR_NAME,
    ROLE_ADMINISTRATOR_CODE,
    ROLE_USER_NAME,
    ROLE_USER_CODE,
    Organization,
    OrganizationInvitation,
    OrganizationRole,
    OrganizationMember,
    User,
    db,
)


def find_user_by_email(email):
    """ Find a user by their email, or return None """
    return User.query.filter(User.email == email).one_or_none()


def find_user_by_reset_token(reset_token):
    """ Find a user by their reset token, or return None """
    return User.query.filter(User.reset_token == reset_token).one_or_none()


def find_user_by_uuid(user_uuid):
    """ Find a user by their UUID, or return None """
    return User.query.filter(User.uuid == user_uuid).one_or_none()


def find_organization_by_uuid(organization_uuid):
    """ Find an organization by their uuid, or return None """
    return Organization.query.filter(
        Organization.uuid == organization_uuid, Organization.is_deleted == False
    ).one_or_none()


def find_organization_by_id(organization_id):
    """ Find an organization by their uuid, or return None """
    return Organization.query.filter(
        Organization.id == organization_id, Organization.is_deleted == False
    ).one_or_none()


def find_pending_invitations_by_organization(organization):
    return OrganizationInvitation.query.filter(
        OrganizationInvitation.organization == organization,
        OrganizationInvitation.accepted == False,
        OrganizationInvitation.cancelled == False,
        OrganizationInvitation.rejected == False,
    ).all()


def find_invitation_by_invitation_uuid(invitation_uuid):
    """ Find an invitation by the invitation token, or return None """
    return OrganizationInvitation.query.filter(
        OrganizationInvitation.uuid == invitation_uuid,
        OrganizationInvitation.accepted == False,
        OrganizationInvitation.cancelled == False,
        OrganizationInvitation.rejected == False,
    ).one_or_none()


def find_invitation_by_invitation_token(invitation_token):
    """ Find an invitation by the invitation token, or return None """
    return OrganizationInvitation.query.filter(
        OrganizationInvitation.invitation_token == invitation_token,
        OrganizationInvitation.accepted == False,
        OrganizationInvitation.cancelled == False,
        OrganizationInvitation.rejected == False,
    ).one_or_none()


def find_invitation_by_email_and_organization(email_address, organization):
    """ Find an invitation for a user, in an organization """
    return OrganizationInvitation.query.filter(
        OrganizationInvitation.email_address == email_address,
        OrganizationInvitation.organization == organization,
        OrganizationInvitation.accepted == False,
        OrganizationInvitation.cancelled == False,
        OrganizationInvitation.rejected == False,
    ).one_or_none()


def is_user_organization_admin(organization, user):
    member_role = find_organization_member_role(organization, user)
    return member_role and member_role.code == ROLE_ADMINISTRATOR_CODE


def find_organization_member_role(organization, user):
    om = OrganizationMember.query.filter(
        OrganizationMember.is_deleted == False,
        OrganizationMember.organization == organization,
        OrganizationMember.user == user,
    ).one_or_none()

    if om:
        return om.organization_role


def find_organization_members(organization):
    return OrganizationMember.query.filter(
        OrganizationMember.is_deleted == False,
        OrganizationMember.organization == organization,
    )


def find_user_organization_memberships(user):
    return OrganizationMember.query.filter(
        OrganizationMember.is_deleted == False, OrganizationMember.user == user
    )


def find_organization_membership(organization, user):
    return OrganizationMember.query.filter(
        OrganizationMember.is_deleted == False,
        OrganizationMember.organization == organization,
        OrganizationMember.user == user,
    ).one_or_none()


def find_organization_role(role_code):
    """Find a specific OrganizationRole.

    If the Role doesn't exist, create it and return it.
    """
    if role_code != ROLE_USER_CODE and role_code != ROLE_ADMINISTRATOR_CODE:
        raise BadRequestError("No user associated with invitation exists!")

    organization_role = OrganizationRole.query.filter(
        OrganizationRole.code == role_code
    ).one_or_none()
    if organization_role is None:
        name = (
            ROLE_USER_NAME if role_code == ROLE_USER_CODE else ROLE_ADMINISTRATOR_NAME
        )
        organization_role = OrganizationRole(
            uuid=uuid.uuid4().hex,
            name=name,
            code=role_code,
        )
        db.session.add(organization_role)

    return organization_role
