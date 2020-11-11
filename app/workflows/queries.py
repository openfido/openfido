from .models import (
    OrganizationWorkflow,
    OrganizationWorkflowPipeline,
    OrganizationWorkflowPipelineRun,
    db,
)


def find_organization_workflows(organization_uuid):
    """ Fetcha all OrganizationWorkflows associated with an organization """
    return OrganizationWorkflow.query.filter(
        OrganizationWorkflow.organization_uuid == organization_uuid,
        OrganizationWorkflow.is_deleted == False,
    ).all()
