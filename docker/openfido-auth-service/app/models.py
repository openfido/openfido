from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

from .utils import to_iso8601

Base = declarative_base()
db = SQLAlchemy()

ROLE_ADMINISTRATOR_NAME = "Administrator"
ROLE_ADMINISTRATOR_CODE = "ADMINISTRATOR"
ROLE_USER_NAME = "User"
ROLE_USER_CODE = "USER"


class User(db.Model):
    """ A User Model """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), nullable=False, server_default="")
    is_system_admin = db.Column(db.Boolean, nullable=False, default=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(127), nullable=False)
    password_salt = db.Column(db.String(127), nullable=False)
    reset_token = db.Column(db.String(32), nullable=True)
    reset_token_expires_at = db.Column(
        db.DateTime, nullable=True, default=lambda: datetime.utcnow()
    )
    last_active_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.utcnow()
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.utcnow()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    organization_memberships = db.relationship(
        "OrganizationMember", backref="user", lazy="dynamic"
    )

    def __repr__(self):
        return f"<User {self.id}: {self.email}>"

    def serialize(self):
        """ Serialize User Object Without an Org """

        return {
            "uuid": self.uuid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "last_active_at": to_iso8601(self.last_active_at),
            "created_at": to_iso8601(self.created_at),
            "updated_at": to_iso8601(self.updated_at),
            "is_system_admin": self.is_system_admin,
        }


class Organization(db.Model):
    """ Org DB Model Class """

    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), nullable=False, server_default="")
    name = db.Column(db.String(60), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.utcnow()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    organization_invitations = db.relationship(
        "OrganizationInvitation", backref="organization", lazy="dynamic"
    )
    organization_members = db.relationship(
        "OrganizationMember", backref="organization", lazy="dynamic"
    )
    organization_invitations = db.relationship(
        "OrganizationInvitation", backref="organization", lazy="immediate"
    )

    def serialize(self):
        """ Serialize User Object (with or without Org) """
        return {
            "uuid": self.uuid,
            "name": self.name,
            "created_at": to_iso8601(self.created_at),
            "updated_at": to_iso8601(self.updated_at),
        }


class OrganizationMember(db.Model):
    """ A member of an organization """

    __tablename__ = "organization_member"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), nullable=False, server_default="")
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    organization_role_id = db.Column(
        db.Integer, db.ForeignKey("organization_role.id"), nullable=False
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.utcnow()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    def serialize_organization_role(self):
        """ Serialize OrganizationMember """
        result = self.organization.serialize()
        result["role"] = {
            "uuid": self.organization_role.uuid,
            "name": self.organization_role.name,
            "code": self.organization_role.code,
        }
        return result

    def serialize_user_role(self):
        """ Serialize OrganizationMember """
        result = self.user.serialize()
        result["role"] = {
            "uuid": self.organization_role.uuid,
            "name": self.organization_role.name,
            "code": self.organization_role.code,
        }
        return result

    def role_enum(self):
        return (self.organization_role.name, self.organization_role.code)


class OrganizationRole(db.Model):
    """ A specific role in an organization """

    __tablename__ = "organization_role"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), nullable=False, server_default="")
    name = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.utcnow()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    organization_members = db.relationship(
        "OrganizationMember", backref="organization_role", lazy="immediate"
    )

    def role_enum(self):
        return (self.name, self.code)


class OrganizationInvitation(db.Model):
    """ An invitation to an email to join an invitation. """

    __tablename__ = "organization_invitations"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), nullable=False, server_default="")
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id"), nullable=False
    )
    email_address = db.Column(db.String(255), nullable=False)
    invitation_token = db.Column(db.String(32), nullable=False, server_default="")
    accepted = db.Column("accepted", db.Boolean, default=False)
    cancelled = db.Column("cancelled", db.Boolean, default=False)
    rejected = db.Column("rejected", db.Boolean, default=False)

    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.utcnow()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    def serialize(self):
        """ Serialize public fields for the API """
        result = {
            "uuid": self.uuid,
            "email_address": self.email_address,
            "organization_uuid": self.organization.uuid,
            "created_at": to_iso8601(self.created_at),
            "updated_at": to_iso8601(self.updated_at),
        }

        return result
