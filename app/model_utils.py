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

    # Pipeline queued, but not ready to start yet (workflow celery task will
    # determine when proper input requirements have been satisfied to transition
    # to NOT_STARTED)
    QUEUED = 1
    # Pipeline has been put on the celery queue, but a worker has not yet picked
    # up the job.
    NOT_STARTED = 2
    # Pipeline is running on a celery worker.
    RUNNING = 3
    # Pipeline failed.
    FAILED = 4
    # Pipeline successfully completed.
    COMPLETED = 5
    # Pipeline ABORTED from QUEUED state (its inputs were never satisfied)
    ABORTED = 6

    def is_valid_transition(self, next_enum):
        """ Return True when the current transition is valid. """
        if self == RunStateEnum.QUEUED:
            return next_enum in [RunStateEnum.NOT_STARTED, RunStateEnum.ABORTED]
        if self == RunStateEnum.NOT_STARTED:
            return next_enum in [RunStateEnum.RUNNING, RunStateEnum.ABORTED]
        if self == RunStateEnum.RUNNING:
            return next_enum in [
                RunStateEnum.FAILED,
                RunStateEnum.COMPLETED,
                RunStateEnum.ABORTED,
            ]

        return False

    def in_final_state(self):
        """ Returns True when this state can't transition to any other. """
        return self in [
            RunStateEnum.FAILED,
            RunStateEnum.COMPLETED,
            RunStateEnum.ABORTED,
        ]


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
