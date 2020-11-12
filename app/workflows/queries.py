from app.workflows.models import (
    OrganizationWorkflow,
)


def find_organization_workflows(organization_uuid):
    """ Fetcha all OrganizationWorkflows associated with an organization """
    return OrganizationWorkflow.query.filter(
        OrganizationWorkflow.organization_uuid == organization_uuid,
        OrganizationWorkflow.is_deleted == False,
    ).all()


def find_organization_workflow(organization_uuid, workflow_uuid):
    """ Fetcha an OrganizationWorkflows associated with an organization """
    return OrganizationWorkflow.query.filter(
        OrganizationWorkflow.organization_uuid == organization_uuid,
        OrganizationWorkflow.is_deleted == False,
        OrganizationWorkflow.uuid == workflow_uuid,
    ).one_or_none()
