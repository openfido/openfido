from .models import Pipeline, PipelineRun, RunStateType, db
from sqlalchemy import and_


def find_pipeline(uuid):
    """ Find a pipelines """
    return Pipeline.query.filter(
        and_(
            Pipeline.uuid == uuid,
            Pipeline.is_deleted == False,
        )
    ).one_or_none()


def find_pipelines():
    """ Find all pipelines """
    return Pipeline.query.filter(Pipeline.is_deleted == False)


def find_run_state_type(run_state):
    """Find a specific RunStateType.

    If the RunStateType doesn't exist, create it and return it.
    """
    run_state_type = RunStateType.query.filter(
        RunStateType.code == run_state.value
    ).one_or_none()
    if run_state_type is None:
        run_state_type = RunStateType(
            name=run_state.name,
            description=run_state.name,
            code=run_state.value,
        )
        db.session.add(run_state_type)

    return run_state_type


def find_pipeline_run(uuid):
    """ Find a PipelineRun. """
    return (
        PipelineRun.query.join(Pipeline)
        .filter(
            and_(
                PipelineRun.uuid == uuid,
                Pipeline.is_deleted == False,
            )
        )
        .one_or_none()
    )
