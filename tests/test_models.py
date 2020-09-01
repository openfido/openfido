from app.models import db, Pipeline, PipelineRun


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
