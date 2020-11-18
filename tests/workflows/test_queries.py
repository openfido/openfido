from ..conftest import ORGANIZATION_UUID, WORKFLOW_UUID
from app.workflows.queries import (
    find_organization_workflow,
    find_organization_workflows,
    find_organization_workflow_pipeline,
    find_organization_workflow_pipelines,
)
from app.workflows.models import db


def test_find_organization_workflows(app, organization_workflow):
    assert set(
        find_organization_workflows(organization_workflow.organization_uuid)
    ) == set([organization_workflow])

    organization_workflow.is_deleted = True
    db.session.commit()

    assert set(
        find_organization_workflows(organization_workflow.organization_uuid)
    ) == set([])


def test_find_organization_workflow(app, organization_workflow):
    assert (
        find_organization_workflow(
            organization_workflow.organization_uuid, organization_workflow.uuid
        )
        == organization_workflow
    )

    organization_workflow.is_deleted = True
    db.session.commit()

    assert (
        find_organization_workflow(
            organization_workflow.organization_uuid, organization_workflow.uuid
        )
        is None
    )


def test_find_organization_workflow_pipelines(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    from app.workflows.models import (
        OrganizationWorkflow,
        OrganizationWorkflowPipeline,
    )

    assert list(
        find_organization_workflow_pipelines(
            organization_workflow.uuid, organization_pipeline.id
        )
    ) == [organization_workflow_pipeline]


def test_find_organization_workflow_pipeline(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    assert (
        find_organization_workflow_pipeline(
            organization_workflow.uuid, organization_workflow_pipeline.uuid
        )
        == organization_workflow_pipeline
    )
