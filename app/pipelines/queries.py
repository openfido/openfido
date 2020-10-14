from app.pipelines.models import OrganizationPipeline, db


def find_organization_pipelines(organization_uuid):
    """ Fetcha all OrganizationPipelines associated with an organization """
    return OrganizationPipeline.query.filter(
        OrganizationPipeline.organization_uuid == organization_uuid
    )
