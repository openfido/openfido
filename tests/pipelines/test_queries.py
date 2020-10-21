from ..conftest import ORGANIZATION_UUID, PIPELINE_UUID
from app.pipelines.queries import (
    find_organization_pipeline,
    find_organization_pipelines,
)
from app.pipelines.models import db


def test_find_organization_pipelines(app, organization_pipeline):
    assert set(
        find_organization_pipelines(organization_pipeline.organization_uuid)
    ) == set([organization_pipeline])

    # deleted pipelines are not included
    organization_pipeline.is_deleted = True
    db.session.commit()
    assert set(
        find_organization_pipelines(organization_pipeline.organization_uuid)
    ) == set([])


def test_find_organization_pipeline(app, organization_pipeline):
    assert (
        find_organization_pipeline(
            organization_pipeline.organization_uuid, organization_pipeline.uuid
        )
        == organization_pipeline
    )

    # deleted pipelines are not returned
    organization_pipeline.is_deleted = True
    db.session.commit()
    assert (
        find_organization_pipeline(
            organization_pipeline.organization_uuid, organization_pipeline.uuid
        )
        is None
    )
