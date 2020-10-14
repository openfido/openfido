from ..conftest import ORGANIZATION_UUID, PIPELINE_UUID
from app.pipelines.queries import (
    find_organization_pipeline,
    find_organization_pipelines,
)
from app.pipelines.models import db


def test_find_organization_pipelines(app, pipeline):
    assert set(find_organization_pipelines(pipeline.organization_uuid)) == set(
        [pipeline]
    )

    # deleted pipelines are not included
    pipeline.is_deleted = True
    db.session.commit()
    assert set(find_organization_pipelines(pipeline.organization_uuid)) == set([])


def test_find_organization_pipeline(app, pipeline):
    assert (
        find_organization_pipeline(pipeline.organization_uuid, pipeline.uuid)
        == pipeline
    )

    # deleted pipelines are not returned
    pipeline.is_deleted = True
    db.session.commit()
    assert find_organization_pipeline(pipeline.organization_uuid, pipeline.uuid) is None
