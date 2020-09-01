import uuid
from enum import Enum, unique

from app.model_utils import CommonColumnsMixin, get_db

db = get_db()


class Application(CommonColumnsMixin, db.Model):
    """ An application registered with a permission. """

    __tablename__ = "application"

    name = db.Column(db.String(50), nullable=False)
    api_key = db.Column(
        db.String(32),
        nullable=False,
        server_default="",
        default=lambda: uuid.uuid4().hex,
    )

    application_system_permissions = db.relationship("ApplicationSystemPermission", backref="application", lazy="select")


class SystemPermission(CommonColumnsMixin, db.Model):
    """ A lookup table of specific permissions supported """

    __tablename__ = "systempermission"

    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.Integer, nullable=False)

    application_system_permissions = db.relationship("ApplicationSystemPermission", backref="system_permission", lazy="select")


class ApplicationSystemPermission(CommonColumnsMixin, db.Model):
    """ A specific permission """

    __tablename__ = "applicationsystempermission"

    application_id = db.Column(
        db.Integer, db.ForeignKey("application.id"), nullable=False
    )
    system_permission_id = db.Column(
        db.Integer, db.ForeignKey("systempermission.id"), nullable=False
    )
