import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CommonColumnsMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.String(32),
        nullable=False,
        server_default="",
        default=lambda: uuid.uuid4().hex,
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


class Pipeline(CommonColumnsMixin, db.Model):
    """ Represents a 'pipeline' job. """

    __tablename__ = "pipeline"

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    docker_image_url = db.Column(db.String(2000), nullable=True)
    repository_ssh_url = db.Column(db.String(2000), nullable=True)
    repository_branch = db.Column(db.String(100), nullable=True)
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)
