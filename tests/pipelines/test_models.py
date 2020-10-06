from app.pipelines.models import db, OrganizationPipeline


def test_organization_pipeline(app):
    op = OrganizationPipeline(organization_uuid="0" * 32, pipeline_uuid="1" * 32)
    db.session.add(op)
    db.session.commit()

    assert op.uuid is not None
