from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest
from freezegun import freeze_time

from app import services, utils
from app.models import db, OrganizationMember, ROLE_ADMINISTRATOR_CODE, ROLE_USER_CODE
from app.queries import find_organization_role, find_organization_members

from .conftest import ORG_NAME, USER_PASSWORD

USER1_EMAIL = "user@example.com"
A_PASSWORD = "apassword!"
A_FIRST = "Danny"
A_LAST = "Fitzgerald"
NEW_ORG_NAME = "friends"


def test_create_user_validate_email(app, organization, user):
    # When no email is provided a ValueError is raised
    db.session.add(user)
    db.session.add(organization)
    db.session.commit()
    with pytest.raises(ValueError):
        services.create_user("", A_PASSWORD, A_FIRST, A_LAST)

    # When an invalid email is provided a ValueError is raised.
    with pytest.raises(ValueError):
        services.create_user("bad@@example.com", A_PASSWORD, A_FIRST, A_LAST)


def test_create_user_validate_password(app, organization):
    db.session.add(organization)
    db.session.commit()
    # When a password of length < 10 is provided, a ValueError is raised.
    with pytest.raises(ValueError):
        services.create_user(USER1_EMAIL, "", A_FIRST, A_LAST)
    with pytest.raises(ValueError):
        services.create_user(USER1_EMAIL, "123456789", A_FIRST, A_LAST)

    # When a password of length >= 10 is provided, a user is created:
    assert services.create_user(USER1_EMAIL, "1234567890", A_FIRST, A_LAST) is not None


def test_create_user_validate_first_name(app):
    # When no first name is provided, a ValueError is raised.
    with pytest.raises(ValueError):
        services.create_user(USER1_EMAIL, A_PASSWORD, None, A_LAST)
    with pytest.raises(ValueError):
        services.create_user(USER1_EMAIL, A_PASSWORD, "", A_LAST)


def test_create_user_validate_last_name(app):
    # When no last name is provided, a ValueError is raised.
    with pytest.raises(ValueError):
        services.create_user(USER1_EMAIL, A_PASSWORD, A_FIRST, None)
    with pytest.raises(ValueError):
        services.create_user(USER1_EMAIL, A_PASSWORD, A_FIRST, "")


def test_create_user(app, organization):
    # Given: good email/passwords are provided, a user is saved
    user = services.create_user(USER1_EMAIL, A_PASSWORD, A_FIRST, A_LAST)
    # Then: a user is created, with email and password hash.
    assert user.email == USER1_EMAIL
    assert user.password_hash != A_PASSWORD
    assert user.first_name == A_FIRST
    assert user.last_name == A_LAST
    assert len(user.password_salt) > 0
    # and the hash would return true if verified
    assert utils.verify_hash(A_PASSWORD, user.password_hash, user.password_salt)


def test_update_user(app, organization):
    user = services.create_user(USER1_EMAIL, A_PASSWORD, A_FIRST, A_LAST)

    user = services.update_user(user, "bob@email.com", "Bob", "Thomas")

    assert user.first_name == "Bob"
    assert user.last_name == "Thomas"
    assert user.email == "bob@email.com"


def test_update_user_validate_email(app, organization):
    user = services.create_user(USER1_EMAIL, A_PASSWORD, A_FIRST, A_LAST)

    with pytest.raises(ValueError):
        # badly formatted email
        services.update_user(user, "ttt", "Bob", "Thomas")

    with pytest.raises(TypeError):
        # no email
        services.update_user(user, "Bob", "Thomas")

    with pytest.raises(ValueError):
        # None type
        services.update_user(user, None, "Bob", "Thomas")


def test_update_user_validate_first_name(app, organization):
    user = services.create_user(USER1_EMAIL, A_PASSWORD, A_FIRST, A_LAST)

    with pytest.raises(ValueError):
        # badly formatted first_name
        services.update_user(user, "tom@email.com", 1, "Thomas")

    with pytest.raises(TypeError):
        # no first_name
        services.update_user(user, "tom@email.com", "Thomas")

    with pytest.raises(ValueError):
        # None type for first_name
        services.update_user(user, "tom@email.com", None, "Thomas")


def test_update_user_validate_last_name(app, organization):
    user = services.create_user(USER1_EMAIL, A_PASSWORD, A_FIRST, A_LAST)

    with pytest.raises(ValueError):
        # badly formatted first_name
        services.update_user(user, "tom@email.com", "Bob", 1)

    with pytest.raises(TypeError):
        # no first_name
        services.update_user(user, "tom@email.com", "Bob")

    with pytest.raises(ValueError):
        # None type for first_name
        services.update_user(user, "tom@email.com", "Bob", None)


def test_update_user_validate_last_name(app, organization):
    user = services.create_user(USER1_EMAIL, A_PASSWORD, A_FIRST, A_LAST)

    with pytest.raises(ValueError):
        # badly formatted first_name
        services.update_user(user, 1, "Bob", "Thomas")

    with pytest.raises(TypeError):
        # no first_name
        services.update_user(user, "Bob", "Thomas")

    with pytest.raises(ValueError):
        # None type for first_name
        services.update_user(user, None, "Bob", "Thomas")


def test_update_user_validate_user(app, organization):
    user = services.create_user(USER1_EMAIL, A_PASSWORD, A_FIRST, A_LAST)

    with pytest.raises(ValueError):
        # badly formatted user
        services.update_user(1, "bob@email.com", "Bob", "Thomas")

    with pytest.raises(TypeError):
        # no user
        services.update_user("bob@email.com", "Bob", "Thomas")

    with pytest.raises(ValueError):
        # None type for first_name
        services.update_user(None, "bob@email.com", "Bob", "Thomas")


# TODO improper organization creation
# def test_create_organization(app, user, organization):
#     # You need a user to create an organization
#     organization = services.create_organization(ORG_NAME)
#
#     assert organization.name == ORG_NAME
#     assert [om.user for om in organization.organization_members] == [user]


def test_delete_organization(app, organization):
    # You need a user to create an organization
    db.session.add(organization)
    db.session.commit()
    organization = services.delete_organization(organization)

    assert organization.is_deleted == True


def test_update_organization(app, organization):
    db.session.add(organization)
    db.session.commit()
    organization = services.update_organization(organization, NEW_ORG_NAME)

    assert organization.name == NEW_ORG_NAME


def test_remove_organization_member_missing_data(app, organization, user):
    with pytest.raises(ValueError):
        services.remove_organization_member(None, user)
    with pytest.raises(ValueError):
        services.remove_organization_member(organization, None)


def test_remove_organization_member(organization, user, admin):
    organization.organization_members.append(
        OrganizationMember(
            user=user,
            organization=organization,
            organization_role=find_organization_role(ROLE_USER_CODE),
        )
    )
    organization_two = services.create_organization("test two")
    organization_two.organization_members.append(
        OrganizationMember(
            user=user,
            organization=organization_two,
            organization_role=find_organization_role(ROLE_USER_CODE),
        )
    )
    db.session.commit()

    assert user in [om.user for om in organization.organization_members]

    services.remove_organization_member(organization, user)

    members = find_organization_members(organization)
    assert user not in [om.user for om in members]


def test_remove_organization_member_must_belong(organization, user, admin):
    organization.organization_members.append(
        OrganizationMember(
            user=user,
            organization=organization,
            organization_role=find_organization_role(ROLE_USER_CODE),
        )
    )
    db.session.commit()

    user_two = services.create_user("user@email.com", "password10chars", "tom", "smith")

    with pytest.raises(ValueError):
        services.remove_organization_member(organization, user_two)


def test_request_password_reset_email_down(app, organization, monkeypatch):
    # Given: existing user, matching password
    user = services.create_user(USER1_EMAIL, A_PASSWORD, A_FIRST, A_LAST)
    db.session.add(user)
    db.session.commit()
    driver_mock = Mock()
    driver_mock.send_reset_email.return_value = False
    monkeypatch.setattr(services.mail, "make_driver", lambda: driver_mock)

    # Then: the user's reset_token is updated, and an email is sent.
    assert not services.request_password_reset(user)
    driver_mock.send_reset_email.assert_called_once()


def test_request_password_reset(app, organization, monkeypatch):
    # Given: existing user, matching password
    user = services.create_user(USER1_EMAIL, A_PASSWORD, A_FIRST, A_LAST)
    db.session.add(user)
    db.session.commit()
    driver_mock = Mock()
    monkeypatch.setattr(services.mail, "make_driver", lambda: driver_mock)

    # Then: the user's reset_token is updated, and an email is sent.
    original_reset_token = user.reset_token
    assert services.request_password_reset(user)
    driver_mock.send_reset_email.assert_called_once()
    assert driver_mock.mock_calls[0][1][0].id == user.id
    assert user.reset_token != original_reset_token
    assert user.reset_token_expires_at < datetime.utcnow()


def test_reset_password_no_reset_token(app, user, organization):
    assert services.request_password_reset(user)
    with pytest.raises(ValueError):
        services.reset_password(user, A_PASSWORD, "not right")


def test_reset_password_bad_password(app, user):
    assert services.request_password_reset(user)
    reset_token = user.reset_token
    with pytest.raises(ValueError):
        services.reset_password(user, "tooshort", user.reset_token)
    # and the token can be used again:
    assert user.reset_token == reset_token


def test_reset_password_expired_token(app, user):
    # Given: user with matching reset_token and password
    assert services.request_password_reset(user)

    # Then: no update b/c the reset_token is expired
    with freeze_time(
        datetime.utcnow() + timedelta(hours=services.RESET_TOKEN_EXPIRATION_HOURS + 1)
    ), pytest.raises(ValueError):
        services.reset_password(user, A_PASSWORD, user.reset_token)

    utils.verify_hash(A_PASSWORD, user.password_hash, user.password_salt)


def test_reset_password(app, user):
    # Given: user with matching reset_token and password
    assert services.request_password_reset(user)
    services.reset_password(user, A_PASSWORD, user.reset_token)

    # Then: the user's password is updated and the reset_token cannot be reused.
    assert utils.verify_hash(A_PASSWORD, user.password_hash, user.password_salt)
    assert user.reset_token == ""


def test_create_invitation(app, user, admin, organization):
    invitation = services.create_invitation(organization, user.email)

    assert invitation.email_address == user.email
    assert invitation.accepted == False
    assert organization == invitation.organization


def test_create_invitation_validate_organization(app, user, admin, organization):
    with pytest.raises(utils.BadRequestError):
        invitation = services.create_invitation("", user.email)


def test_create_invitation_validate_already_invited(app, user, admin, organization):
    services.create_invitation(organization, user.email)
    with pytest.raises(utils.BadRequestError):
        services.create_invitation(organization, user.email)


def test_change_password_bad_password(app, user):
    with pytest.raises(ValueError):
        services.change_password(user, USER_PASSWORD, "tooshort")


def test_change_password(app, user):
    # Given: user with matching reset_token and password
    services.change_password(user, USER_PASSWORD, A_PASSWORD)

    # Then: the user's password is updated and the reset_token cannot be reused.
    assert utils.verify_hash(A_PASSWORD, user.password_hash, user.password_salt)


def test_accept_invitation_error(app, organization, user):
    no_user_email = "nouser@example.com"
    invitation = services.create_invitation(organization, no_user_email)
    with pytest.raises(ValueError):
        services.accept_invitation("no-token")

    with pytest.raises(ValueError):
        services.accept_invitation(invitation.invitation_token)

    organization.organization_members.append(
        OrganizationMember(
            user=user,
            organization=organization,
            organization_role=find_organization_role(ROLE_USER_CODE),
        )
    )
    invitation = services.create_invitation(organization, user.email)
    with pytest.raises(ValueError):
        services.accept_invitation(invitation.invitation_token)


def test_accept_invitation(app, organization, user):
    invitation = services.create_invitation(organization, user.email)
    services.accept_invitation(invitation.invitation_token)
