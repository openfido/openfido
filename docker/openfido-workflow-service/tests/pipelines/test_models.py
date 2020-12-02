from unittest.mock import MagicMock, patch

from app.pipelines.models import db, Pipeline, PipelineRun, PipelineRunArtifact
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


def test_create_pipeline_run(app, pipeline):
    pipeline_run = PipelineRun(sequence=1)
    pipeline.pipeline_runs.append(pipeline_run)
    db.session.add(pipeline)
    db.session.commit()

    assert set(PipelineRun.query.all()) == set([pipeline_run])


@patch("app.pipelines.models.create_url")
def test_public_url(create_url_mock, app, pipeline):
    create_url_mock.return_value = "http://example.com/presigned"

    pipeline_run = PipelineRun(sequence=1)
    pipeline.pipeline_runs.append(pipeline_run)
    artifact = PipelineRunArtifact(name="example.txt")
    pipeline_run.pipeline_run_artifacts.append(artifact)
    db.session.add(pipeline)
    db.session.commit()

    assert artifact.public_url() == "http://example.com/presigned"
