from app.pipelines.models import db, OrganizationPipeline


def test_organization_pipeline(app, pipeline):
    assert pipeline.uuid is not None
