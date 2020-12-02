from ..conftest import ORGANIZATION_UUID, PIPELINE_UUID
from app.pipelines.queries import (
    find_organization_pipeline,
    find_organization_pipeline_by_id,
    find_organization_pipelines,
    find_organization_pipeline_input_files,
    find_organization_pipeline_run,
    find_latest_organization_pipeline_run,
    search_organization_pipeline_input_files,
    search_organization_pipeline_runs,
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


def test_find_organization_pipeline_by_id(app, organization_pipeline):
    assert (
        find_organization_pipeline_by_id(organization_pipeline.id)
        == organization_pipeline
    )


def test_search_organization_pipeline_input_files(
    app, organization_pipeline, organization_pipeline_input_file
):
    assert search_organization_pipeline_input_files(
        organization_pipeline.id, [organization_pipeline_input_file.uuid]
    ) == [organization_pipeline_input_file]


def test_find_organization_pipeline_input_files(
    app, organization_pipeline, organization_pipeline_input_file
):
    assert find_organization_pipeline_input_files(organization_pipeline.id) == [
        organization_pipeline_input_file
    ]


def test_find_organization_pipeline_run(
    app, organization_pipeline, organization_pipeline_run
):

    pipeline_run = find_organization_pipeline_run(
        organization_pipeline.id, organization_pipeline_run.pipeline_run_uuid
    )

    assert pipeline_run == organization_pipeline_run


def test_find_latest_organization_pipeline_run(
    app, organization_pipeline, organization_pipeline_run
):

    pipeline_run = find_organization_pipeline_run(
        organization_pipeline.id, organization_pipeline_run.pipeline_run_uuid
    )

    assert pipeline_run == organization_pipeline_run


def test_search_organization_pipeline_runs(
    app, organization_pipeline, organization_pipeline_run
):

    pipeline_run = search_organization_pipeline_runs(
        organization_pipeline.id, [organization_pipeline_run.pipeline_run_uuid]
    )

    assert pipeline_run == [organization_pipeline_run]
