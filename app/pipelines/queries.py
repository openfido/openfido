from app.pipelines.models import (
    OrganizationPipeline,
    OrganizationPipelineInputFile,
    OrganizationPipelineRun,
    db,
)


def find_organization_pipelines(organization_uuid):
    """ Fetcha all OrganizationPipelines associated with an organization """
    return OrganizationPipeline.query.filter(
        OrganizationPipeline.organization_uuid == organization_uuid,
        OrganizationPipeline.is_deleted == False,
    )


def find_organization_pipeline(organization_uuid, organization_pipeline_uuid):
    """ Fetcha a OrganizationPipeline """
    return OrganizationPipeline.query.filter(
        OrganizationPipeline.organization_uuid == organization_uuid,
        OrganizationPipeline.uuid == organization_pipeline_uuid,
        OrganizationPipeline.is_deleted == False,
    ).one_or_none()


def find_organization_pipeline_input_files(organization_pipeline_id):
    """ Search for Organization Pipeline Input Files """
    return OrganizationPipelineInputFile.query.filter(
        OrganizationPipelineInputFile.organization_pipeline_id
        == organization_pipeline_id
    ).all()


def search_organization_pipeline_input_files(organization_pipeline_id, uuids):
    """ Find Organization Pipeline Input Files """
    return OrganizationPipelineInputFile.query.filter(
        OrganizationPipelineInputFile.organization_pipeline_id
        == organization_pipeline_id,
        OrganizationPipelineInputFile.uuid.in_(uuids),
    ).all()
