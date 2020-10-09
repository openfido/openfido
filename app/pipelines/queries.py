from app.pipelines.models import OrganizationPipeline, db


def find_organization_pipelines(organization_uuid):
    """ Fetcha all OrganizationPipelines associated with an organization """
    return OrganizationPipeline.query.filter(
        OrganizationPipeline.organization_uuid == organization_uuid
    )


def find_organization_pipeline(organization_uuid, organization_pipeline_uuid):
    """ Fetcha a OrganizationPipeline """
    return OrganizationPipeline.query.filter(
        OrganizationPipeline.organization_uuid == organization_uuid,
        OrganizationPipeline.uuid == organization_pipeline_uuid,
    ).one_or_none()
