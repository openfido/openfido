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


@patch("app.pipelines.models.get_s3")
def test_public_url(get_s3_mock, app, pipeline):
    s3_mock = MagicMock()
    get_s3_mock.return_value = s3_mock
    s3_mock.generate_presigned_url.return_value = "http://example.com/presigned"

    pipeline_run = PipelineRun(sequence=1)
    pipeline.pipeline_runs.append(pipeline_run)
    artifact = PipelineRunArtifact(name="example.txt")
    pipeline_run.pipeline_run_artifacts.append(artifact)
    db.session.add(pipeline)
    db.session.commit()

    assert artifact.public_url() == "http://example.com/presigned"
