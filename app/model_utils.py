import importlib
import os
import uuid
from datetime import datetime
from enum import IntEnum, unique

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@unique
class SystemPermissionEnum(IntEnum):
    """ All possible types of SystemPermission for Pipelines """

    PIPELINES_CLIENT = 1
    PIPELINES_WORKER = 2


@unique
class RunStateEnum(IntEnum):
    """ Run states currently supported in PipelineRunState """

    NOT_STARTED = 1
    RUNNING = 2
    FAILED = 3
    COMPLETED = 4

    def is_valid_transition(self, next_enum):
        """ Return True when the current transition is valid. """
        if self == RunStateEnum.NOT_STARTED:
            return next_enum is RunStateEnum.RUNNING
        if self == RunStateEnum.RUNNING:
            return next_enum in set([RunStateEnum.FAILED, RunStateEnum.COMPLETED])

        return False


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
