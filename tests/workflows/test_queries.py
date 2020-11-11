from ..conftest import ORGANIZATION_UUID, WORKFLOW_UUID
from app.workflows.queries import (
    find_organization_workflows,
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
