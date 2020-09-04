from enum import IntEnum, unique

from flask_sqlalchemy import SQLAlchemy
from .model_utils import get_db, CommonColumnsMixin

db = get_db()


class Pipeline(CommonColumnsMixin, db.Model):
    """ Represents a 'pipeline' job. """

    __tablename__ = "pipeline"

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    docker_image_url = db.Column(db.String(2000), nullable=True)
    repository_ssh_url = db.Column(db.String(2000), nullable=True)
    repository_branch = db.Column(db.String(100), nullable=True)
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)

    pipeline_runs = db.relationship("PipelineRun", backref="pipeline", lazy="select")


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


class RunStateType(CommonColumnsMixin, db.Model):
    """ Lookup table of run states. """

    __tablename__ = "runstatetype"

    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    code = db.Column(db.Numeric(), nullable=False)

    pipeline_run_states = db.relationship(
        "PipelineRunState", backref="run_state_type", lazy="immediate"
    )


class PipelineRunState(CommonColumnsMixin, db.Model):
    """ Lookup table of run states. """

    __tablename__ = "pipelinerunstate"

    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    run_state_type_id = db.Column(
        db.Integer, db.ForeignKey("runstatetype.id"), nullable=False
    )
    pipeline_run_id = db.Column(
        db.Integer, db.ForeignKey("pipelinerun.id"), nullable=False
    )


class PipelineRunArtifact(CommonColumnsMixin, db.Model):
    """ An artifact created by a PipelineRun. """

    __tablename__ = "pipelinerunartifact"

    name = db.Column(db.String(255), nullable=False)

    pipeline_run_id = db.Column(
        db.Integer, db.ForeignKey("pipelinerun.id"), nullable=False
    )


class PipelineRunInput(CommonColumnsMixin, db.Model):
    """ Inputs used to execute a PipelineRun. """

    __tablename__ = "pipelineruninput"

    filename = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(2000), nullable=False)

    pipeline_run_id = db.Column(
        db.Integer, db.ForeignKey("pipelinerun.id"), nullable=False
    )


class PipelineRun(CommonColumnsMixin, db.Model):
    """ A pipeline run """

    __tablename__ = "pipelinerun"

    sequence = db.Column(db.Integer, nullable=False)
    worker_ip = db.Column(db.String(50), nullable=True)
    callback_url = db.Column(db.String(2000), nullable=True)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    std_out = db.Column(db.Unicode, nullable=True)
    std_err = db.Column(db.Unicode, nullable=True)

    pipeline_id = db.Column(db.Integer, db.ForeignKey("pipeline.id"), nullable=False)

    pipeline_run_states = db.relationship(
        "PipelineRunState", backref="pipeline_run", lazy="immediate"
    )
    pipeline_run_artifacts = db.relationship(
        "PipelineRunArtifact", backref="pipeline_run", lazy="immediate"
    )
    pipeline_run_inputs = db.relationship(
        "PipelineRunInput", backref="pipeline_run", lazy="immediate"
    )
