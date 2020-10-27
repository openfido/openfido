"""Organization endpoint tests
"""
import io

from unittest.mock import patch
from app import queries
from app.models import (
    OrganizationInvitation,
    User,
    db,
    ROLE_ADMINISTRATOR_CODE,
    ROLE_USER_CODE,
)
from app.queries import (
    find_invitation_by_invitation_token,
    find_organization_member_role,
)
from app.services import (
    create_organization,
    delete_organization,
    create_invitation,
    cancel_invitation,
    reject_invitation,
    accept_invitation,
)
from app.utils import to_iso8601, BadRequestError
from freezegun import freeze_time

from .conftest import ADMIN_PASSWORD, USER_PASSWORD, ORG_NAME


def test_create_organization(client, admin_auth_token):
    response = client.post(
        "/organizations",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={
            "name": ORG_NAME,
        },
    )

    assert response.status_code == 200


def test_create_organization_missing_name_param(client, admin_auth_token):
    response = client.post(
        "/organizations",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={},
    )

    assert response.status_code == 400


def test_create_organization_invalid_name_param(client, admin_auth_token):
    response = client.post(
        "/organizations",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={"name": "a"},
    )

    assert response.status_code == 400


def test_delete_organization(
    client,
    organization_admin,
    organization_admin_auth_token,
    organization,
    admin_auth_token,
):
    response = client.delete(
        "/organizations/" + organization.uuid,
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
    )
    assert response.status_code == 200

    response = client.get(
        "/organizations/" + organization.uuid + "/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={},
    )

    assert response.status_code == 400


def test_delete_organization_invalid_organization_uuid(client, admin_auth_token):
    response = client.delete(
        "/organizations/notarealuuid",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
    )

    assert response.status_code == 400


@patch("app.org.services.delete_organization")
def test_delete_organization_bad_error(
    delete_org_mock, client, admin_auth_token, organization
):
    delete_org_mock.side_effect = BadRequestError("err")
    response = client.delete(
        "/organizations/" + organization.uuid,
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
    )

    assert response.status_code == 400


def test_delete_organization_not_system_admin(client, user_auth_token, organization):
    response = client.delete(
        "/organizations/" + organization.uuid,
        headers={
            "Content-Type": "application/json",
            "Authorization": user_auth_token,
        },
    )

    assert response.status_code == 401


def test_update_organization(client, organization_admin_auth_token, organization):
    NEW_ORG_NAME = "Updated Org Name"
    response = client.put(
        f"/organizations/{organization.uuid}/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={
            "name": NEW_ORG_NAME,
        },
    )

    assert response.json["name"] == NEW_ORG_NAME
    assert response.status_code == 200


def test_update_organization_invalid_organization_uuid(
    client, organization_admin_auth_token
):
    response = client.put(
        "/organizations/notarealuuid/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={
            "name": "updated org name",
        },
    )

    assert response.status_code == 400


def test_update_organization_missing_name_parameter(
    client, organization_admin_auth_token, organization
):
    response = client.put(
        "/organizations/" + organization.uuid + "/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={},
    )

    assert response.status_code == 400


def test_update_organization_not_org_admin(client, user, user_auth_token, organization):
    NEW_ORG_NAME = "Updated Org Name"
    invitation = create_invitation(organization, user.email)
    accept_invitation(invitation.invitation_token)

    response = client.put(
        "/organizations/" + organization.uuid + "/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": user_auth_token,
        },
        json={
            "name": NEW_ORG_NAME,
        },
    )

    assert response.status_code == 401


def test_update_organization_invalid_name_param(
    client, organization, organization_admin_auth_token
):
    response = client.put(
        "/organizations/" + organization.uuid + "/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={
            "name": "A",
        },
    )

    assert response.status_code == 400


def test_update_organization_logo_401(
    client, organization, user_auth_token, organization_admin_auth_token
):
    # user is not an organization administrator
    response = client.put(
        "/organizations/" + organization.uuid + "/logo",
        headers={"Content-Type": "image/png", "Authorization": user_auth_token},
        data="fakeimagedata",
    )

    assert response.status_code == 401

    # no auth provided
    response = client.put(
        "/organizations/" + organization.uuid + "/logo",
        headers={"Content-Type": "image/png"},
        data="fakeimagedata",
    )

    assert response.status_code == 401

    # invalid organization uuid
    response = client.put(
        "/organizations/invaliduuid/logo",
        headers={
            "Content-Type": "image/png",
            "Authorization": organization_admin_auth_token,
        },
        data="fakeimagedata",
    )

    assert response.status_code == 401


@patch("app.org.services.update_organization_logo")
def test_update_organization_logo_failure(
    update_org_logo_mock,
    client,
    organization,
    user_auth_token,
    organization_admin_auth_token,
):
    update_org_logo_mock.side_effect = BadRequestError("err")
    response = client.put(
        f"/organizations/{organization.uuid}/logo",
        headers={
            "Content-Type": "image/png",
            "Authorization": organization_admin_auth_token,
        },
        data="fakeimagedata",
    )

    assert response.status_code == 400


@patch("app.org.services.update_organization_logo")
def test_update_organization_logo(
    update_org_logo_mock,
    client,
    organization,
    user_auth_token,
    organization_admin_auth_token,
):
    response = client.put(
        f"/organizations/{organization.uuid}/logo",
        headers={
            "Content-Type": "image/png",
            "Authorization": organization_admin_auth_token,
        },
        data="fakeimagedata",
    )

    assert response.status_code == 200


def test_get_organization_logo_401(client, organization, user_auth_token):
    response = client.get(
        "/organizations/" + organization.uuid + "/logo",
    )

    assert response.status_code == 401

    response = client.get(
        "/organizations/invaliduuid/logo",
        headers={"Authorization": user_auth_token},
    )

    assert response.status_code == 401


@patch("app.org.services.get_organization_logo")
def test_get_organization_logo_bad_error(
    get_org_logo_mock, client, organization, admin_auth_token
):
    get_org_logo_mock.side_effect = BadRequestError("err")
    response = client.get(
        "/organizations/" + organization.uuid + "/logo",
        headers={
            "Authorization": admin_auth_token,
        },
    )

    assert response.status_code == 400


@patch("app.org.services.get_organization_logo")
def test_get_organization_logo_bad_error(
    get_org_logo_mock, client, organization, admin_auth_token
):
    get_org_logo_mock.return_value = io.StringIO("some data")
    response = client.get(
        "/organizations/" + organization.uuid + "/logo",
        headers={
            "Authorization": admin_auth_token,
        },
    )

    assert response.status_code == 200


def test_user_has_organization_200(client, admin, admin_auth_token):
    """/organzations HTTP 200 organization has admin user"""
    response = client.post(
        "/organizations",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={"name": ORG_NAME},
    )
    membership = admin.organization_memberships.first()

    # assert that on creation, an organization is added to a User
    assert response.json["name"] == membership.organization.name
    assert membership.organization_role.code == ROLE_ADMINISTRATOR_CODE


def test_get_organization_profile(client, organization, organization_admin_auth_token):
    response = client.get(
        "/organizations/" + organization.uuid + "/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={},
    )

    assert response.status_code == 200


def test_get_organization_profile_invalid_organization_uuid(
    client, organization_admin_auth_token
):
    response = client.get(
        "/organizations/notarealuuid/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={},
    )

    assert response.status_code == 400


def test_get_organization_profile_not_member(client, organization, user_auth_token):
    response = client.get(
        "/organizations/" + organization.uuid + "/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": user_auth_token,
        },
        json={},
    )

    assert response.status_code == 401


def test_get_organization_members_200(
    client, organization_admin_auth_token, organization
):
    """/organizations/:org_uuid/members HTTP 200"""
    response = client.get(
        f"/organizations/{organization.uuid}/members",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
    )

    assert response.status_code == 200


def test_get_organization_members_400(client, admin_auth_token):
    org_uuid = "1234"

    response = client.get(
        "/organizations/" + org_uuid + "/members",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={},
    )

    assert response.status_code == 400


def test_get_organization_members_401(client, user_auth_token, organization):
    """/organizations/:org_uuid/members HTTP 401"""

    response = client.get(
        f"/organizations/{organization.uuid}/members",
        headers={
            "Content-Type": "application/json",
            "Authorization": user_auth_token,
        },
        json={},
    )

    assert response.status_code == 401


def test_get_users_organizations_200(client, user, user_auth_token):
    """/users/:user_uuid/organizations HTTP 200"""

    organization = create_organization("test org", user)
    organization_two = create_organization("test org2", user)
    organization_three = create_organization("test org3", user)

    # create the test org as an admin
    response = client.get(
        f"/users/{user.uuid}/organizations",
        headers={
            "Content-Type": "application/json",
            "Authorization": user_auth_token,
        },
    )
    assert response.status_code == 200
    assert len(response.json) == 3
    assert response.json[0]["name"] == organization.name
    assert response.json[1]["name"] == organization_two.name
    assert response.json[2]["name"] == organization_three.name

    delete_organization(organization)
    response = client.get(
        f"/users/{user.uuid}/organizations",
        headers={
            "Content-Type": "application/json",
            "Authorization": user_auth_token,
        },
    )
    assert response.status_code == 200
    assert len(response.json) == 2


def test_get_users_organizations_401(client, admin, admin_auth_token):
    response = client.get(
        "/users/" + "123123123" + "/organizations",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
    )

    assert response.status_code == 401


def test_invite_organization_member_400(
    client, organization_admin, organization_admin_auth_token, organization
):
    """/organzations/:organization_uuid/invitations HTTP 400"""

    # user is already a member
    result = client.post(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={"email": organization_admin.email},
    )
    assert result.status_code == 400

    # bad organization id here should return organization not found
    result = client.post(
        f"/organizations/{'0' * 32}/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={},
    )
    assert result.status_code == 400

    result = client.post(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={"email": ""},
    )
    assert result.status_code == 400

    result = client.post(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={"email": 1235},
    )
    assert result.status_code == 400

    # request does not contains email for organization being updated
    result = client.post(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={},
    )
    assert result.status_code == 400

    # request does not contains email for organization being updated
    result = client.post(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={"email": "thisstringisnotanemail"},
    )
    assert result.status_code == 400


def test_invite_organization_member_401(
    client, user, admin, organization, user_auth_token
):
    """/organzations/:organization_uuid/invitations HTTP 401"""
    # bad organization id here should return organization not found
    result = client.post(
        "/organizations/" + "123123123" + "/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": "",
        },
        json={},
    )
    assert result.status_code == 401

    # request does not contains auth token
    result = client.post(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
        },
        json={"email": admin.email},
    )
    assert result.status_code == 401

    # request does not contains valid auth token
    result = client.post(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": user_auth_token,
        },
        json={"email": admin.email},
    )
    assert result.status_code == 401


def test_list_organization_invitaions_200(
    client, user, organization, organization_admin, organization_admin_auth_token
):
    invitation = create_invitation(organization, user.email)
    org2 = create_organization("org2", organization_admin)
    invitation2 = create_invitation(org2, user.email)

    result = client.get(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
    )

    assert result.status_code == 200
    assert (
        len(list(filter(lambda i: i["email_address"] == user.email, result.json))) == 1
    )
    assert user.email in [i["email_address"] for i in result.json]


def test_list_organization_invitaions_no_accepted_invitations(
    client, user, organization, organization_admin_auth_token
):
    invitation = create_invitation(organization, user.email)
    accept_invitation(invitation.invitation_token)

    result = client.get(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
    )

    assert result.status_code == 200
    assert not user.email in [i["email_address"] for i in result.json]


def test_list_organization_invitaions_no_rejected_invitations(
    client, user, organization, organization_admin_auth_token
):
    invitation = create_invitation(organization, user.email)
    reject_invitation(invitation.invitation_token)

    result = client.get(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
    )

    assert result.status_code == 200
    assert not user.email in [i["email_address"] for i in result.json]


def test_list_organization_invitaions_no_cancelled_invitations(
    client, user, organization, organization_admin_auth_token
):
    invitation = create_invitation(organization, user.email)
    cancel_invitation(invitation.uuid)

    result = client.get(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
    )

    assert result.status_code == 200
    assert not user.email in [i["email_address"] for i in result.json]


def test_list_organization_invitations_400(client, user, admin, admin_auth_token):
    """/organzations/:organization_uuid/invitations HTTP 400"""
    # bad organization id here should return organization not found
    result = client.get(
        "/organizations/123123123/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={},
    )
    assert result.status_code == 400

    # bad organization id here should return organization not found
    result = client.get(
        "/organizations/123123123/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={},
    )
    assert result.status_code == 400


def test_list_organization_invitaions_401(
    client, user, admin, organization, admin_auth_token, user_auth_token
):
    """/organzations/:organization_uuid/invitations HTTP 401"""
    invitation = create_invitation(organization, admin.email)
    # try to get that user's organizations
    result = client.get(
        "/organizations/123123123/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": "",
        },
        json={},
    )
    assert result.status_code == 401

    # request does not contains auth token
    result = client.get(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
        },
        json=[{"email": admin.email}],
    )
    assert result.status_code == 401

    # request does not contains valid auth token
    result = client.get(
        f"/organizations/{organization.uuid}/invitations",
        headers={
            "Content-Type": "application/json",
            "Authorization": user_auth_token,
        },
        json=[{"email": admin.email}],
    )
    assert result.status_code == 401


def test_accept_organization_invitation(client, user):
    organization = create_organization("New Org")
    invitation = create_invitation(organization, user.email)

    result = client.post(
        f"/organizations/invitations/accept",
        headers={
            "Content-Type": "application/json",
        },
        json={"invitation_token": "incorrecttoken"},
    )
    assert result.status_code == 400

    result = client.post(
        f"/organizations/invitations/accept",
        headers={
            "Content-Type": "application/json",
        },
        json={"invitation_token": invitation.invitation_token},
    )
    # admin is already in organization invited to
    assert result.json["organization_uuid"] == organization.uuid
    assert result.status_code == 200
    assert user in [om.user for om in user.organization_memberships]


def test_reject_organization_invitation(client, user):
    organization = create_organization("New Org")
    invitation = create_invitation(organization, user.email)

    result = client.post(
        f"/organizations/invitations/reject",
        headers={
            "Content-Type": "application/json",
        },
        json={"invitation_token": "incorrecttoken"},
    )
    assert result.status_code == 400

    result = client.post(
        f"/organizations/invitations/reject",
        headers={
            "Content-Type": "application/json",
        },
        json={"invitation_token": invitation.invitation_token},
    )
    assert result.status_code == 200

    result = client.post(
        f"/organizations/invitations/accept",
        headers={
            "Content-Type": "application/json",
        },
        json={"invitation_token": invitation.invitation_token},
    )
    assert result.status_code == 400

    assert not user in [om.user for om in user.organization_memberships]


def test_cancel_organization_invitation(client, user, admin, admin_auth_token):
    organization = create_organization("New Org", admin)
    invitation = create_invitation(organization, user.email)

    result = client.post(
        f"/organizations/invitations/cancel",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={"invitation_uuid": "incorrectuuid"},
    )
    assert result.status_code == 400

    result = client.post(
        f"/organizations/invitations/cancel",
        headers={
            "Content-Type": "application/json",
            "Authorization": "invalidbearertoken",
        },
        json={"invitation_uuid": invitation.uuid},
    )
    assert result.status_code == 401

    result = client.post(
        f"/organizations/invitations/cancel",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={"invitation_uuid": invitation.uuid},
    )
    assert result.status_code == 200

    result = client.post(
        f"/organizations/invitations/accept",
        headers={
            "Content-Type": "application/json",
        },
        json={"invitation_uuid": invitation.uuid},
    )
    assert result.status_code == 400

    assert not user in [om.user for om in user.organization_memberships]


def test_change_organization_member_role(
    client, organization, organization_user, organization_admin_auth_token
):
    result = client.put(
        f"/organizations/{organization.uuid}/members/{organization_user.uuid}/role",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={"role": ROLE_ADMINISTRATOR_CODE},
    )
    assert result.status_code == 200
    assert (
        find_organization_member_role(organization, organization_user).code
        == ROLE_ADMINISTRATOR_CODE
    )


def test_change_organization_member_role_400(
    client, organization, user, organization_user, organization_admin_auth_token
):
    # invalid organization uuid should fail
    result = client.put(
        f"/organizations/invalidorgid/members/{organization_user.uuid}/role",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={"role": ROLE_ADMINISTRATOR_CODE},
    )
    assert result.status_code == 400

    # invalid user uuid should fail
    result = client.put(
        f"/organizations/{organization.uuid}/members/invaliduserid/role",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={"role": ROLE_ADMINISTRATOR_CODE},
    )
    assert result.status_code == 400

    # invalid role should fail
    result = client.put(
        f"/organizations/{organization.uuid}/members/{organization_user.uuid}/role",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={"role": "invalidrolecode"},
    )
    assert result.status_code == 400

    # target user is not a member should fail
    result = client.put(
        f"/organizations/{organization.uuid}/members/{user.uuid}/role",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={"role": ROLE_ADMINISTRATOR_CODE},
    )
    assert result.status_code == 400

    # target user already has the requested role should fail
    result = client.put(
        f"/organizations/{organization.uuid}/members/{organization_user.uuid}/role",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={"role": ROLE_USER_CODE},
    )
    assert result.status_code == 400


def test_change_organization_member_role_401(
    client, organization, organization_user, organization_user_auth_token
):
    result = client.put(
        f"/organizations/{organization.uuid}/members/{organization_user.uuid}/role",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_user_auth_token,
        },
        json={"role": ROLE_ADMINISTRATOR_CODE},
    )
    assert result.status_code == 401


def test_remove_organization_member_200(
    client, user, organization_admin, organization_admin_auth_token
):
    organization = create_organization("test org", organization_admin)
    invitation = create_invitation(organization, user.email)
    accept_invitation(invitation.invitation_token)

    response = client.delete(
        f"/organizations/{organization.uuid}" f"/members/{user.uuid}",
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
    )

    assert response.status_code == 200
    members = queries.find_organization_members(organization)
    assert user not in [om.user for om in members]


def test_remove_organization_member_no_org(client, user, admin_auth_token):
    response = client.delete(
        f"/organizations/badid/members/{user.uuid}",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
    )
    assert response.status_code == 400


def test_remove_organization_member_no_user(client, organization, admin_auth_token):
    db.session.add(organization)
    db.session.commit()
    response = client.delete(
        f"/organizations/{organization.uuid}/members/badid",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
    )
    assert response.status_code == 401


def test_remove_organization_member_400(
    client, user, admin, organization, admin_auth_token
):
    # creating a new organization, so admin has 2 organizations
    create_organization_response = client.post(
        "/organizations",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={
            "name": ORG_NAME,
        },
    )

    # create a second user for the organization
    # organization now has two users in it
    create_user_response = client.post(
        "/users",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={
            "email": "user2@email.com",
            "password": "testpassword2",
            "last_name": "Test",
            "first_name": "Johnny",
        },
    )

    remove_url = (
        f"/organizations/{create_organization_response.json['uuid']}"
        f"/members/{create_user_response.json['uuid']}"
    )

    remove_member_response = client.delete(
        remove_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={},
    )

    new_org = queries.find_user_by_uuid(create_organization_response.json["uuid"])

    assert create_organization_response.status_code == 200
    assert create_user_response.status_code == 200
    assert remove_member_response.status_code == 400


def test_remove_organization_member_user_not_in_org_400(
    client, organization, user, organization_admin_auth_token
):
    remove_url = f"/organizations/{organization.uuid}" f"/members/{user.uuid}"
    response = client.delete(
        remove_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": organization_admin_auth_token,
        },
        json={},
    )

    assert response.status_code == 400
