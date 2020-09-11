from app.models import db, Pipeline, PipelineRun
from app.model_utils import RunStateEnum


def test_create_pipeline(app):
    """ A new pipeline model does save to the database. """
    pipeline = Pipeline(
        name="a pipeline",
        description="a description",
    )
    db.session.add(pipeline)
    db.session.commit()

    assert set(Pipeline.query.all()) == set([pipeline])
    assert len(pipeline.uuid) > 0
    assert not pipeline.is_deleted


def test_create_pipeline_run(app):
    pipeline = Pipeline(
        name="a pipeline",
        description="a description",
    )
    pipeline_run = PipelineRun(sequence=1)
    pipeline.pipeline_runs.append(pipeline_run)
    db.session.add(pipeline)
    db.session.commit()

    assert set(PipelineRun.query.all()) == set([pipeline_run])


def test_run_state_is_valid_transition(app):
    assert not RunStateEnum.NOT_STARTED.is_valid_transition(RunStateEnum.NOT_STARTED)
    assert RunStateEnum.NOT_STARTED.is_valid_transition(RunStateEnum.RUNNING)

    assert not RunStateEnum.RUNNING.is_valid_transition(RunStateEnum.RUNNING)
    assert not RunStateEnum.RUNNING.is_valid_transition(RunStateEnum.NOT_STARTED)
    assert RunStateEnum.RUNNING.is_valid_transition(RunStateEnum.FAILED)
    assert RunStateEnum.RUNNING.is_valid_transition(RunStateEnum.COMPLETED)

    assert not RunStateEnum.FAILED.is_valid_transition(RunStateEnum.NOT_STARTED)
    assert not RunStateEnum.FAILED.is_valid_transition(RunStateEnum.RUNNING)
    assert not RunStateEnum.FAILED.is_valid_transition(RunStateEnum.FAILED)
    assert not RunStateEnum.FAILED.is_valid_transition(RunStateEnum.COMPLETED)

    assert not RunStateEnum.COMPLETED.is_valid_transition(RunStateEnum.NOT_STARTED)
    assert not RunStateEnum.COMPLETED.is_valid_transition(RunStateEnum.RUNNING)
    assert not RunStateEnum.COMPLETED.is_valid_transition(RunStateEnum.FAILED)
    assert not RunStateEnum.COMPLETED.is_valid_transition(RunStateEnum.COMPLETED)
