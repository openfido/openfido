from app.pipelines.models import OrganizationPipeline
from app.workflows.models import (
    OrganizationWorkflow,
    OrganizationWorkflowPipeline,
    OrganizationWorkflowRun,
    OrganizationWorkflowPipelineRun,
)


def find_organization_workflows(organization_uuid):
    """ Fetches all OrganizationWorkflows associated with an organization """
    return OrganizationWorkflow.query.filter(
        OrganizationWorkflow.organization_uuid == organization_uuid,
        OrganizationWorkflow.is_deleted == False,
    ).all()


def find_organization_workflow(organization_uuid, organization_workflow_uuid):
    """ Fetches an OrganizationWorkflows associated with an organization """
    return OrganizationWorkflow.query.filter(
        OrganizationWorkflow.organization_uuid == organization_uuid,
        OrganizationWorkflow.is_deleted == False,
        OrganizationWorkflow.uuid == organization_workflow_uuid,
    ).one_or_none()


def find_organization_workflow_pipelines(
    organization_workflow_uuid, organization_pipeline_id
):
    """Fetches all OrganizationWorkflowPipelines associated with an organization pipeline. """
    return OrganizationWorkflowPipeline.query.filter(
        OrganizationWorkflowPipeline.organization_workflow_uuid
        == organization_workflow_uuid,
        OrganizationPipeline.id == organization_pipeline_id,
        OrganizationWorkflowPipeline.is_deleted == False,
    )


def find_organization_workflow_pipeline(
    organization_workflow_uuid, organization_workflow_pipeline_uuid
):
    """Fetches an OrganizationWorkflowPipeline associated with an organization pipeline. """
    return OrganizationWorkflowPipeline.query.filter(
        OrganizationWorkflowPipeline.organization_workflow_uuid
        == organization_workflow_uuid,
        OrganizationWorkflowPipeline.uuid == organization_workflow_pipeline_uuid,
        OrganizationWorkflowPipeline.is_deleted == False,
    ).one_or_none()


def find_organization_workflow_run(
    organization_workflow_uuid, organization_workflow_run_uuid
):
    """Fetches an OrganizationWorkflowRun"""
    return OrganizationWorkflowRun.query.filter(
        OrganizationWorkflowRun.organization_workflow_uuid
        == organization_workflow_uuid,
        OrganizationWorkflowRun.uuid == organization_workflow_run_uuid,
        OrganizationWorkflowRun.is_deleted == False,
    ).one_or_none()


def find_organization_workflow_pipeline_run_by_workflow_run_uuid(workflow_run_uuid):
    """Fetches an OrganizationWorkflowPipelineRun by workflow run uuid. """
    return OrganizationWorkflowPipelineRun.query.filter(
        OrganizationWorkflowPipelineRun.workflow_run_uuid == workflow_run_uuid
    ).one_or_none()
