import importlib
import os
import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_db(path=os.environ.get("SQLACHEMY_DB_INSTANCE", None)):
    if path is None:
        return db

    db_import = importlib.import_module(path)
    return db_import.db


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
