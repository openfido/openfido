import importlib
import os
import uuid as uuid_lib
from datetime import datetime
from enum import IntEnum, unique

from flask_sqlalchemy import SQLAlchemy


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
    # Pipeline CANCELLED from QUEUED state (its inputs were never satisfied)
    CANCELLED = 6

    def is_valid_transition(self, next_enum):
        """ Return True when the current transition is valid. """
        if self == RunStateEnum.QUEUED:
            return next_enum in [RunStateEnum.NOT_STARTED, RunStateEnum.CANCELLED]
        if self == RunStateEnum.NOT_STARTED:
            return next_enum in [RunStateEnum.RUNNING, RunStateEnum.CANCELLED]
        if self == RunStateEnum.RUNNING:
            return next_enum in [
                RunStateEnum.FAILED,
                RunStateEnum.COMPLETED,
                RunStateEnum.CANCELLED,
            ]

        return False

    def in_final_state(self):
        """ Returns True when this state can't transition to any other. """
        return self in [
            RunStateEnum.FAILED,
            RunStateEnum.COMPLETED,
            RunStateEnum.CANCELLED,
        ]
