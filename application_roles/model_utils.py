import importlib
import os
import uuid as uuid_lib
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_db(path=os.environ.get("SQLACHEMY_DB_INSTANCE", None)):
    """ Get access to an instance of the SqlAchemy database. """
    if path is None:
        return db

    db_import = importlib.import_module(path)
    return db_import.db


class CommonColumnsMixin:
    """ id, uuid, created_at and updated_at SqlAchemy mixin. """

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.String(32),
        nullable=False,
        server_default="",
        default=lambda: uuid_lib.uuid4().hex,
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
