import json
import time
from datetime import datetime, timedelta

from app import auth
from app.auth import handle_error
from app.models import db
from app.utils import decode_jwt, make_jwt, verify_jwt
from app.queries import find_user_by_email
from app.services import (
    create_invitation,
)
from freezegun import freeze_time

from .conftest import (
    ADMIN_PASSWORD,
    TOMORROW,
    USER_PASSWORD,
    USER_TWO_PASSWORD,
    ORG_NAME,
)

# Getting secrets from the .env file
# uses python's dotenv

ADMIN_TOKEN = ""

USER1_EMAIL = "user@example.com"
USER2_EMAIL = "user2@example.com"
CREATE_USER_EMAIL = "imanewuser@email.com"
CREATE_USER_PASSWORD = "tencharpassword"


def test_seed_user(client, admin):
    # note that a user sequence table has to be created and active in the flask environment
    # this is normally done when a new user is created, but since it's seed data in a migraion
    # there will be an error until ID 2 is created.
    # Temp solution is to just hit the create endpoint twice.
    #
    #    accountservices=# select * from users_id_seq;
    #    last_value | log_cnt | is_called
    #   ------------+---------+-----------
    #             2 |      31 | t
    #   (1 row)

    # Authenticate with seed admin
    # POST http://localhost:5000/users/auth
    db.session.add(admin)
    db.session.commit()

    admin_seed_response = ""
    admin_seed_response = client.post(
        "/users/auth",
        headers={
            "Content-Type": "application/json",
        },
        json={"email": admin.email, "password": ADMIN_PASSWORD},
    )
    assert admin_seed_response.status_code == 200


def test_error_auth_headers_no_content_type(client, admin):
    admin_seed_response = ""
    admin_seed_response = client.post(
        "/users/auth",
        headers={
            "Content-Type": "",
        },
        json={"email": admin.email, "password": ADMIN_PASSWORD},
    )
    assert admin_seed_response.status_code == 400


def test_error_auth_headers_bad_content_type(client, admin):
    admin_seed_response = ""
    admin_seed_response = client.post(
        "/users/auth",
        headers={
            "Content-Type-BAD": "",
        },
        json={"email": admin.email, "password": ADMIN_PASSWORD},
    )
    assert admin_seed_response.status_code == 200


def test_create_user_bad_json(client, admin_auth_token):
    result = client.post(
        "/users",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        data='{"email": "blah",}',
    )
    assert result.status_code == 400


def test_create_user_for_system_admin(client, admin, admin_auth_token):
    # using an admin's token, creating a new user

    response = client.post(
        "/users",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={
            "email": CREATE_USER_EMAIL,
            "password": CREATE_USER_PASSWORD,
            "last_name": "Test",
            "first_name": "Johnny",
        },
    )
    assert response.status_code == 200

    response = client.post(
        "/users/auth",
        headers={
            "Content-Type": "application/json",
        },
        json={
            "email": CREATE_USER_EMAIL,
            "password": CREATE_USER_PASSWORD,
        },
    )
    assert response.status_code == 200


def test_create_user_with_invitation_token(client, organization):
    invitation = create_invitation(organization, CREATE_USER_EMAIL)

    create_user_response = client.post(
        "/users",
        headers={
            "Content-Type": "application/json",
        },
        json={
            "email": CREATE_USER_EMAIL,
            "password": CREATE_USER_PASSWORD,
            "last_name": "Test",
            "first_name": "Johnny",
            "invitation_token": invitation.invitation_token,
        },
    )
    assert create_user_response.status_code == 200
    user = find_user_by_email(CREATE_USER_EMAIL)
    assert user in [om.user for om in user.organization_memberships]
    assert organization in [om.organization for om in user.organization_memberships]

    response = client.post(
        "/users/auth",
        headers={
            "Content-Type": "application/json",
        },
        json={
            "email": CREATE_USER_EMAIL,
            "password": CREATE_USER_PASSWORD,
        },
    )
    assert response.status_code == 200


def test_create_user_with_invalid_invitation_token(client, organization):
    create_invitation(organization, CREATE_USER_EMAIL)

    response = client.post(
        "/users",
        headers={
            "Content-Type": "application/json",
        },
        json={
            "email": CREATE_USER_EMAIL,
            "password": CREATE_USER_PASSWORD,
            "last_name": "Test",
            "first_name": "Johnny",
            "invitation_token": "notavalidinvitationtoken",
        },
    )
    assert response.status_code == 400


def test_create_user_with_invitation_token_and_different_email_address(
    client, organization
):
    invitation = create_invitation(organization, CREATE_USER_EMAIL)

    response = client.post(
        "/users",
        headers={
            "Content-Type": "application/json",
        },
        json={
            "email": "nottherightemail@email.com",
            "password": CREATE_USER_PASSWORD,
            "last_name": "Test",
            "first_name": "Johnny",
            "invitation_token": invitation.invitation_token,
        },
    )
    assert response.status_code == 400


def test_create_user_401(client, user, user_auth_token):
    response = client.post(
        "/users",
        headers={"Content-Type": "application/json"},
        json={
            "email": CREATE_USER_EMAIL,
            "password": CREATE_USER_PASSWORD,
            "last_name": "Test",
            "first_name": "Johnny",
        },
    )
    assert response.status_code == 401

    response = client.post(
        "/users",
        headers={
            "Content-Type": "application/json",
            "Authorization": user_auth_token,
        },
        json={
            "email": CREATE_USER_EMAIL,
            "password": CREATE_USER_PASSWORD,
            "last_name": "Test",
            "first_name": "Johnny",
        },
    )
    assert response.status_code == 401


def test_create_user_400(client, admin_auth_token):
    response = client.post(
        "/users",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={
            "email": "badpassword@email.com",
            "password": "123",
            "last_name": "Bad",
            "organizations": "AnyCo",
            "first_name": "Password",
        },
    )
    assert response.status_code == 400


def test_create_user_exists_400(client, user, admin_auth_token):
    response = client.post(
        "/users",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
        json={
            "email": user.email,
            "password": "123",
            "last_name": "User",
            "organizations": "",
            "first_name": "Second",
        },
    )
    assert response.status_code == 400


def test_get_user_200(client, user, user_auth_token, admin_auth_token):
    response = client.get(
        "/users/" + user.uuid + "/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
    )
    assert response.status_code == 401

    response = client.get(
        "/users/" + user.uuid + "/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": user_auth_token,
        },
    )
    assert response.status_code == 200
    assert response.json["uuid"] == user.uuid
    assert response.json["first_name"] == user.first_name
    assert response.json["last_name"] == user.last_name
    assert response.json["email"] == user.email

    # A non-existant user returns a 401
    response = client.get(
        "/users/fdea5bfbfeca40618046178090fe022a/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": admin_auth_token,
        },
    )
    assert response.status_code == 401


def test_update_user_200(client, user, user_auth_token):
    NEW_EMAIL = "email2@email.com"
    NEW_FIRST_NAME = "Joe"
    NEW_LAST_NAME = "Johnson"
    response = client.put(
        "/users/" + user.uuid + "/profile",
        headers={"Content-Type": "application/json", "Authorization": user_auth_token},
        json={
            "email": NEW_EMAIL,
            "first_name": NEW_FIRST_NAME,
            "last_name": NEW_LAST_NAME,
        },
    )

    assert response.status_code == 200
    assert response.json["uuid"] == user.uuid
    assert response.json["first_name"] == NEW_FIRST_NAME
    assert response.json["last_name"] == NEW_LAST_NAME
    assert response.json["email"] == NEW_EMAIL


def test_update_user_400(client, user, user_auth_token):
    response = client.put(
        "/users/" + user.uuid + "/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": user_auth_token,
        },
        json={"first_name": "Joe", "last_name": "Johnson"},
    )

    assert response.status_code == 400


def test_update_user_401(client, user_auth_token, user_two):
    response = client.put(
        "/users/" + user_two.uuid + "/profile",
        headers={
            "Content-Type": "application/json",
            "Authorization": user_auth_token,
        },
        json={"email": "tom@email.com", "first_name": "Joe", "last_name": "Johnson"},
    )

    assert response.status_code == 401


def test_jwt_required(client, user):
    # No authorization header returns a 401
    result = client.post("/users/auth/refresh", content_type="application/json")
    assert result.status_code == 401

    # A non bearer header returns a 401
    result = client.post(
        "/users/auth/refresh",
        content_type="application/json",
        headers={"Authorization": "Basic 123456789"},
    )
    assert result.status_code == 401

    # A badly formatted bearer token returns a 401
    result = client.post(
        "/users/auth/refresh",
        content_type="application/json",
        headers={
            "Authorization": "Bearer eyJ0e  XAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTkzNjI2MjQ5LCJpc3MiOiJhcHAiLCJpYXQiOjE1OTEwMzQyNDl9.-j5K1xiYx6GzyKoI5UsKnpiCA1vF1D5gBreCUlnm01o"
        },
    )
    assert result.status_code == 401

    # An badly formatted JWT token returns a 401
    result = client.post(
        "/users/auth/refresh",
        content_type="application/json",
        headers={
            "Authorization": "Bearer XXXXXXXXXXXKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTkzNjI2MjQ5LCJpc3MiOiJhcHAiLCJpYXQiOjE1OTEwMzQyNDl9.-j5K1xiYx6GzyKoI5UsKnpiCA1vF1D5gBreCUlnm01o"
        },
    )
    assert result.status_code == 401

    # A valid JWT that is expired returns a 401
    db.session.add(user)
    db.session.commit()
    calling_token = make_jwt(user, TOMORROW).decode("utf-8")
    with freeze_time((TOMORROW + timedelta(days=1)).strftime("%Y-%m-%d")):
        result = client.post(
            "/users/auth/refresh",
            content_type="application/json",
            headers={"Authorization": f"Bearer {calling_token}"},
        )
        assert result.status_code == 401

    # A valid JWT token for a user that doesn't exist returns a 401
    db.session.delete(user)
    db.session.commit()
    time.sleep(1)
    result = client.post(
        "/users/auth/refresh",
        content_type="application/json",
        headers={"Authorization": f"Bearer {calling_token}"},
    )
    assert result.status_code == 401


def test_refresh(client, user):
    calling_token = make_jwt(user, TOMORROW).decode("utf-8")
    calling_jwt = decode_jwt(calling_token)

    # A non json contenttype returns a 400
    result = client.post(
        "/users/auth/refresh",
        headers={"Authorization": f"Bearer {calling_token}"},
    )
    assert result.status_code == 400

    # A valid JWT token returns a new token
    # tokens aren't gauranteed to be unique and will be sub-second...so let a
    # little time go by to gaurantee a unique JWT is returned by the endpoint.
    time.sleep(1)
    result = client.post(
        "/users/auth/refresh",
        content_type="application/json",
        headers={"Authorization": f"Bearer {calling_token}"},
    )
    result_jwt = decode_jwt(result.json["token"])
    assert result.status_code == 200
    assert verify_jwt(user, result.json["token"])
    assert result.json["token"] != calling_token
    # its max-exp always equals the calling_token's value
    assert result_jwt["max-exp"] == calling_jwt["max-exp"]


@freeze_time("2020-05-05")
def test_refresh_max_exp(client, user):
    db.session.add(user)
    db.session.commit()
    calling_token = make_jwt(user, datetime.now()).decode("utf-8")

    # Renewing a token that is older than its max-exp returns a 401
    with freeze_time("2020-05-06"):
        result = client.post(
            "/users/auth/refresh",
            content_type="application/json",
            headers={"Authorization": f"Bearer {calling_token}"},
        )
        assert result.status_code == 401


def test_handleerror(client):
    json, status_code = handle_error("an error")
    assert status_code == 500
    assert json == {}


def test_request_password_reset_no_user(client):
    result = client.post(
        "/users/request_password_reset",
        content_type="application/json",
        json={"email": "bad@example.com"},
    )
    assert result.status_code == 200


def test_request_password_reset_failed_reset(client, user, monkeypatch):
    db.session.add(user)
    db.session.commit()
    monkeypatch.setattr(auth.services, "request_password_reset", lambda x: False)

    result = client.post(
        "/users/request_password_reset",
        content_type="application/json",
        json={"email": user.email},
    )
    assert result.status_code == 400


def test_request_password_reset(client, user, monkeypatch):
    db.session.add(user)
    db.session.commit()
    monkeypatch.setattr(auth.services, "request_password_reset", lambda x: True)

    result = client.post(
        "/users/request_password_reset",
        content_type="application/json",
        json={"email": user.email},
    )
    assert result.status_code == 200


def test_reset_password_no_such_user(client):
    result = client.put(
        "/users/reset_password",
        content_type="application/json",
        json={
            "password": "a_password!",
            "reset_token": "foo",
        },
    )
    assert result.status_code == 400


def test_reset_password_bad_password(client, user):
    user.reset_token = "foo"
    db.session.add(user)
    db.session.commit()

    result = client.put(
        "/users/reset_password",
        content_type="application/json",
        json={
            "password": "short",
            "reset_token": "foo",
        },
    )
    assert result.status_code == 400


def test_reset_password(client, user):
    user.reset_token = "foo"
    db.session.add(user)
    db.session.commit()

    result = client.put(
        "/users/reset_password",
        content_type="application/json",
        json={
            "password": "a_password!",
            "reset_token": "foo",
        },
    )
    assert result.status_code == 200


def test_change_password(client, user, user_auth_token):
    NEW_PASSWORD = "thisisanewpassword"

    response = client.put(
        "/users/password",
        headers={"Content-Type": "application/json", "Authorization": user_auth_token},
        json={"old_password": USER_PASSWORD, "new_password": NEW_PASSWORD},
    )
    assert response.status_code == 200

    response = client.post(
        "/users/auth",
        headers={
            "Content-Type": "application/json",
        },
        json={"email": user.email, "password": NEW_PASSWORD},
    )
    assert response.status_code == 200


def test_change_password_invalid_new_password(client, user, user_auth_token):
    response = client.put(
        "/users/password",
        headers={"Content-Type": "application/json", "Authorization": user_auth_token},
        json={"old_password": USER_PASSWORD, "new_password": "2short"},
    )
    assert response.status_code == 401

    response = client.put(
        "/users/password",
        headers={"Content-Type": "application/json", "Authorization": user_auth_token},
        json={"old_password": USER_PASSWORD, "new_password": USER_PASSWORD},
    )
    assert response.status_code == 401

    response = client.post(
        "/users/auth",
        headers={
            "Content-Type": "application/json",
        },
        json={"email": user.email, "password": USER_PASSWORD},
    )
    assert response.status_code == 200


def test_change_password_invalid_old_password(client, user, organization):
    db.session.add(organization)
    db.session.commit()
    db.session.add(user)
    db.session.commit()

    auth_user_response = client.post(
        "/users/auth",
        headers={
            "Content-Type": "application/json",
        },
        json={"email": user.email, "password": USER_PASSWORD},
    )
    assert auth_user_response.status_code == 200

    USER_TOKEN = auth_user_response.json["token"]
    # building the bearer token
    USER_TOKEN = str("Bearer " + USER_TOKEN)

    change_password_response = client.put(
        "/users/password",
        headers={"Content-Type": "application/json", "Authorization": USER_TOKEN},
        json={"old_password": "incorrect", "new_password": "2short"},
    )
    assert change_password_response.status_code == 401

    auth_user_response = client.post(
        "/users/auth",
        headers={
            "Content-Type": "application/json",
        },
        json={"email": user.email, "password": USER_PASSWORD},
    )
    assert auth_user_response.status_code == 200


def test_change_password_invalid_auth(client, user, organization):
    NEW_PASSWORD = "thisisanewpassword"
    db.session.add(organization)
    db.session.commit()
    db.session.add(user)
    db.session.commit()

    USER_TOKEN = "Bearer ABC1234"
    change_password_response = client.put(
        "/users/password",
        headers={"Content-Type": "application/json", "Authorization": USER_TOKEN},
        json={"old_password": USER_PASSWORD, "new_password": NEW_PASSWORD},
    )
    assert change_password_response.status_code == 401

    auth_user_response = client.post(
        "/users/auth",
        headers={
            "Content-Type": "application/json",
        },
        json={"email": user.email, "password": USER_PASSWORD},
    )
    assert auth_user_response.status_code == 200
