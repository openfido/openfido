import os
import uuid
from datetime import datetime, timedelta

import pytest
from app import create_app
from app.models import (
    ROLE_USER_CODE,
    ROLE_ADMINISTRATOR_CODE,
    User,
    Organization,
    OrganizationInvitation,
    OrganizationMember,
    db,
)
from app.utils import make_hash, make_jwt
from app.queries import find_organization_role
from flanker.addresslib import address
from flask_migrate import upgrade

USER_PASSWORD = "atestpass"
USER_TWO_PASSWORD = "betestpass"
ADMIN_EMAIL = "admin@email.com"
ADMIN_PASSWORD = "123456aoeu7890"
ADMIN_FIRST_NAME = "John"
ADMIN_LAST_NAME = "Smith"
ORG_NAME = "Org1"
TOMORROW = datetime.utcnow() + timedelta(days=1)


@pytest.fixture
def app():
    # create a temporary file to isolate the database for each test
    (app, db, _) = create_app(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "TESTING": True,
            "DEBUG": True,
            "SECRET_KEY": "PYTEST",
            "EMAIL_DRIVER": "null",
        }
    )

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def organization(app):
    organization = Organization(
        uuid=uuid.uuid4().hex,
        name="test org",
    )
    db.session.add(organization)
    db.session.commit()

    return organization


@pytest.fixture
def invitation(app, admin, organization):
    oi = OrganizationInvitation(
        uuid=uuid.uuid4().hex,
        email_address=admin.email,
        organization_id=organization.id,
    )
    db.session.add(oi)
    db.session.commit()
    return oi


@pytest.fixture
def admin(app):
    p_hash, p_salt = make_hash(ADMIN_PASSWORD)
    user = User(
        uuid=uuid.uuid4().hex,
        email=ADMIN_EMAIL,
        first_name=ADMIN_FIRST_NAME,
        last_name=ADMIN_LAST_NAME,
        password_hash=p_hash,
        password_salt=p_salt,
        is_system_admin=True,
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def organization_admin(app, organization):
    p_hash, p_salt = make_hash(USER_PASSWORD)
    user = User(
        uuid=uuid.uuid4().hex,
        email="orgadmin@example.com",
        first_name="firstname",
        last_name="lastname",
        password_hash=p_hash,
        password_salt=p_salt,
        is_system_admin=False,
    )
    db.session.add(user)
    db.session.commit()

    role = find_organization_role(ROLE_ADMINISTRATOR_CODE)
    db.session.add(role)
    db.session.commit()

    membership = OrganizationMember(
        uuid=uuid.uuid4().hex,
        organization_id=organization.id,
        user_id=user.id,
        organization_role_id=role.id,
    )

    db.session.add(membership)
    db.session.commit()
    return user


@pytest.fixture
def organization_user(app, organization):
    p_hash, p_salt = make_hash(USER_PASSWORD)
    user = User(
        uuid=uuid.uuid4().hex,
        email="orguser@example.com",
        first_name="firstname",
        last_name="lastname",
        password_hash=p_hash,
        password_salt=p_salt,
        is_system_admin=False,
    )
    db.session.add(user)
    db.session.commit()

    role = find_organization_role(ROLE_USER_CODE)
    db.session.add(role)
    db.session.commit()

    membership = OrganizationMember(
        uuid=uuid.uuid4().hex,
        organization_id=organization.id,
        user_id=user.id,
        organization_role_id=role.id,
    )

    db.session.add(membership)
    db.session.commit()
    return user


@pytest.fixture
def user(app):
    p_hash, p_salt = make_hash(USER_PASSWORD)
    user = User(
        uuid=uuid.uuid4().hex,
        email="anemail@example.com",
        first_name="firstname",
        last_name="lastname",
        password_hash=p_hash,
        password_salt=p_salt,
        is_system_admin=False,
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def user_two(app):
    p_hash, p_salt = make_hash(USER_TWO_PASSWORD)
    return User(
        uuid=uuid.uuid4().hex,
        email="bob@example.com",
        first_name="Bob",
        last_name="Thomas",
        password_hash=p_hash,
        password_salt=p_salt,
        is_system_admin=False,
    )


@pytest.fixture(autouse=True)
def no_mx_dns_calls(monkeypatch):
    monkeypatch.setattr(address, "validate_address", lambda x: True)


@pytest.fixture()
def user_auth_token(user):
    db.session.add(user)
    db.session.commit()
    return f"Bearer {make_jwt(user, TOMORROW).decode('utf-8')}"


@pytest.fixture()
def admin_auth_token(admin):
    db.session.add(admin)
    db.session.commit()
    return f"Bearer {make_jwt(admin, TOMORROW).decode('utf-8')}"


@pytest.fixture()
def organization_admin_auth_token(organization_admin):
    db.session.add(organization_admin)
    db.session.commit()
    return f"Bearer {make_jwt(organization_admin, TOMORROW).decode('utf-8')}"


@pytest.fixture()
def organization_user_auth_token(organization_user):
    db.session.add(organization_user)
    db.session.commit()
    return f"Bearer {make_jwt(organization_user, TOMORROW).decode('utf-8')}"
