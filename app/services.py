import uuid
from datetime import datetime, timedelta
from email.utils import parseaddr

from flanker.addresslib import address

from . import mail, utils
from .utils import BadRequestError, to_iso8601, get_s3
from .models import (
    ROLE_ADMINISTRATOR_CODE,
    ROLE_USER_CODE,
    Organization,
    OrganizationInvitation,
    OrganizationMember,
    User,
    db,
)
from .queries import (
    find_invitation_by_invitation_uuid,
    find_invitation_by_email_and_organization,
    find_invitation_by_invitation_token,
    find_organization_role,
    find_organization_member_role,
    find_organization_membership,
    find_user_by_email,
    find_organization_by_id,
)

MIN_ORG_NAME_LENGTH = 3
MIN_PASSWORD_LENGTH = 10
RESET_TOKEN_EXPIRATION_HOURS = 24


# user here is the user that is creating the org passed in
def create_organization(name, user=None):
    """Create an Organization.

    If a user is included, add them as an admin to the organization.
    """
    _validate_organization_fields(name)
    organization = Organization(uuid=uuid.uuid4().hex, name=name)
    if user:
        organization.organization_members.append(
            OrganizationMember(
                user=user,
                organization=organization,
                organization_role=find_organization_role(ROLE_ADMINISTRATOR_CODE),
            )
        )
    db.session.add(organization)
    db.session.commit()
    return organization


def update_organization(organization, name):
    """Update an Organization."""
    _validate_organization_fields(name)
    if not isinstance(organization, Organization):
        raise BadRequestError("Invalid organization")

    organization.name = name
    db.session.commit()
    return organization


def delete_organization(organization):
    """Delete an Organization."""
    if not isinstance(organization, Organization):
        raise BadRequestError("Invalid organization")

    for o in organization.organization_members:
        o.is_deleted = True

    for i in organization.organization_invitations:
        if not i.accepted and not i.rejected and not i.cancelled:
            i.is_cancelled = True

    organization.is_deleted = True
    db.session.commit()
    return organization


def create_invitation(organization, email):
    """Create an OrganizationInvitation"""
    _validate_email(email)
    if not isinstance(organization, Organization):
        raise BadRequestError("Invalid organization")

    invitation = find_invitation_by_email_and_organization(email, organization)
    if not invitation:
        invitation = OrganizationInvitation(
            uuid=uuid.uuid4().hex,
            invitation_token=uuid.uuid4().hex,
            email_address=email,
            organization_id=organization.id,
        )
        db.session.add(invitation)
        db.session.commit()

    if not mail.make_driver().send_organization_invitation_email(organization, email, invitation):
        raise BadRequestError("Unable to send invitation email")

    return invitation


def accept_invitation(invitation_token):
    """ Accept an invitation """

    invitation = find_invitation_by_invitation_token(invitation_token)
    if invitation is None:
        raise BadRequestError("No such invitation")

    user = find_user_by_email(invitation.email_address)
    if user is None:
        raise BadRequestError("No user associated with invitation exists!")

    organization = find_organization_by_id(invitation.organization_id)
    if organization in [om.organization for om in user.organization_memberships]:
        raise BadRequestError("User is already in the organization!")

    organization.organization_members.append(
        OrganizationMember(
            uuid=uuid.uuid4().hex,
            user=user,
            organization=organization,
            organization_role=find_organization_role(ROLE_USER_CODE),
        )
    )
    invitation.accepted = True
    db.session.commit()


def reject_invitation(invitation_token):
    """ Accept an invitation """

    invitation = find_invitation_by_invitation_token(invitation_token)
    if invitation is None:
        raise BadRequestError("No such invitation")

    invitation.rejected = True
    db.session.commit()


def cancel_invitation(invitation_uuid):
    """ Accept an invitation """

    invitation = find_invitation_by_invitation_uuid(invitation_uuid)
    if invitation is None:
        raise BadRequestError("No such invitation")

    invitation.cancelled = True
    db.session.commit()


def remove_organization_member(organization, user):
    """ Remove a User from an Organization. """
    if organization is None or not isinstance(organization, Organization):
        raise BadRequestError("Invalid Organization, None Type")
    if user is None or not isinstance(user, User):
        raise BadRequestError("Invalid User, None Type")
    memberships = [om for om in organization.organization_members if om.user == user]
    if len(memberships) == 0:
        raise BadRequestError("User not in Organization!")

    for member in memberships:
        member.is_deleted = True

    db.session.commit()

    return "Member was successfully removed from Organization."


def update_organization_member_role(organization, user, role_code):
    """ Remove a User from an Organization. """
    if organization is None or not isinstance(organization, Organization):
        raise BadRequestError("Invalid organization")
    if user is None or not isinstance(user, User):
        raise BadRequestError("Invalid user")

    membership = find_organization_membership(organization, user)
    if not membership:
        raise BadRequestError("User is not a member")
    if membership.organization_role.code == role_code:
        raise BadRequestError(
            f"User already has role {membership.organization_role.name}"
        )

    new_role = find_organization_role(role_code)
    if new_role is None:
        raise BadRequestError("Invalid role")

    membership.is_deleted = True
    new_membership = OrganizationMember(
        uuid=uuid.uuid4().hex,
        user=user,
        organization=organization,
        organization_role=new_role,
    )
    organization.organization_members.append(new_membership)
    db.session.commit()


def create_user(email, password, first_name, last_name):
    """Create a User.

    Note: The db.session is not committed. Be sure to commit the session.
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        raise BadRequestError(
            f"Passwords must have length of at least {MIN_PASSWORD_LENGTH}"
        )
    _validate_user_fields(email, first_name, last_name)

    p_hash, p_salt = utils.make_hash(password)
    user = User(
        uuid=uuid.uuid4().hex,
        email=email,
        password_hash=p_hash,
        password_salt=p_salt,
        first_name=first_name,
        last_name=last_name,
    )
    db.session.add(user)
    db.session.commit()

    return user


def update_user(user, email, first_name, last_name):
    if not isinstance(user, User):
        raise BadRequestError("Invalid user")
    _validate_user_fields(email, first_name, last_name)

    user.email = email
    user.first_name = first_name
    user.last_name = last_name

    db.session.commit()
    return user


def update_user_last_active_at(user):
    if not isinstance(user, User):
        raise BadRequestError("Invalid user")

    user.last_active_at = datetime.utcnow()
    db.session.commit()
    return user

def update_user_avatar(user, stream):
    if not isinstance(user, User):
        raise BadRequestError("Invalid user")

    s3 = get_s3()
    bucket = current_app.config[S3_BUCKET]
    if bucket not in [b["Name"] for b in s3.list_buckets()["Buckets"]]:
        s3.create_bucket(ACL="private", Bucket=bucket)
    s3.upload_fileobj(
        stream,
        bucket,
        f"avatars/{user.uuid}",
    )

def get_user_avatar(user):
    if not isinstance(user, User):
        raise BadRequestError("Invalid user")
    
    s3 = get_s3()
    bucket = current_app.config[S3_BUCKET]
    if bucket not in [b["Name"] for b in s3.list_buckets()["Buckets"]]:
        s3.create_bucket(ACL="private", Bucket=bucket)

    string_io = StringIO.StringIO()
    filename = f"avatars/{user.uuid}"
    s3.download_file(bucket, filename, string_io)

    return string_io

def update_organization_logo(organization, stream):
    if not isinstance(organization, Organization):
        raise BadRequestError("Invalid organization")

    s3 = get_s3()
    bucket = current_app.config[S3_BUCKET]
    if bucket not in [b["Name"] for b in s3.list_buckets()["Buckets"]]:
        s3.create_bucket(ACL="private", Bucket=bucket)
    s3.upload_fileobj(
        stream,
        bucket,
        f"logos/{user.uuid}",
    )

def get_organization_logo(organization):
    if not isinstance(organization, Organization):
        raise BadRequestError("Invalid organization")
    
    s3 = get_s3()
    bucket = current_app.config[S3_BUCKET]
    if bucket not in [b["Name"] for b in s3.list_buckets()["Buckets"]]:
        s3.create_bucket(ACL="private", Bucket=bucket)

    string_io = StringIO.StringIO()
    filename = f"logos/{user.uuid}"
    s3.download_file(bucket, filename, string_io)

    return string_io

def change_password(user, old_password, new_password):
    if user is None or not isinstance(user, User):
        raise BadRequestError("Invalid user")
    if not utils.verify_hash(old_password, user.password_hash, user.password_salt):
        raise BadRequestError("Incorrect password")

    if old_password == new_password:
        raise BadRequestError("Passwords must be different")

    if len(new_password) < MIN_PASSWORD_LENGTH:
        raise BadRequestError(
            f"Passwords must have length of at least {MIN_PASSWORD_LENGTH}"
        )

    p_hash, p_salt = utils.make_hash(new_password)
    user.password_hash = p_hash
    user.password_salt = p_salt

    db.session.commit()


def request_password_reset(user):
    """Reset a User's password, and send a reset user.

    Returns True on success.
    """
    if not user or not isinstance(user, User):
        raise BadRequestError("Invalid user")
    user.reset_token = uuid.uuid4().hex
    user.reset_token_expires_at = datetime.utcnow()
    db.session.commit()

    return mail.make_driver().send_password_reset_email(user)


def reset_password(user, password, reset_token):
    """Change a user's password."""
    if not user or not isinstance(user, User):
        raise BadRequestError("Invalid user")
    if reset_token != user.reset_token:
        raise BadRequestError("Reset token is not valid")

    expiration = user.reset_token_expires_at.utcnow() + timedelta(
        hours=RESET_TOKEN_EXPIRATION_HOURS
    )
    if expiration < datetime.utcnow():
        raise BadRequestError("reset_token is expired")

    if len(password) < MIN_PASSWORD_LENGTH:
        raise BadRequestError(
            f"Passwords must have length of at least {MIN_PASSWORD_LENGTH}"
        )

    p_hash, p_salt = utils.make_hash(password)
    user.password_hash = p_hash
    user.password_salt = p_salt
    user.reset_token = ""

    db.session.commit()


def _validate_organization_fields(name):
    """ Validate an organization's params fields """
    if not isinstance(name, str):
        raise BadRequestError("Invalid name")
    if len(name) < MIN_ORG_NAME_LENGTH:
        raise BadRequestError(
            f"Organization name must have length of at least {MIN_ORG_NAME_LENGTH}"
        )


def _validate_user_fields(email, first_name, last_name):
    """ Validate a user's params fields """
    if not isinstance(first_name, str):
        raise BadRequestError("Invalid first_name")
    if not isinstance(last_name, str):
        raise BadRequestError("Invalid last_name")
    _validate_email(email)
    if first_name is None or len(first_name) == 0:
        raise BadRequestError("Invalid first_name")
    if last_name is None or len(last_name) == 0:
        raise BadRequestError("Invalid last_name")


def _validate_email(email):
    if not isinstance(email, str) or parseaddr(email) == ("", ""):
        raise BadRequestError("Invalid email")
    if address.parse(email) is None:
        raise BadRequestError("Invalid email")
