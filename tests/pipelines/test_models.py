from app.pipelines.models import db, OrganizationPipeline


def test_organization_pipeline(app, organization_pipeline):
    assert organization_pipeline.uuid is not None
