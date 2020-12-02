from app.pipelines.models import (
    OrganizationPipeline,
    OrganizationPipelineInputFile,
    OrganizationPipelineRun,
    db,
)
from sqlalchemy import and_, or_


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


def find_organization_pipeline_by_id(organization_pipeline_id):
    """ Fetcha a OrganizationPipeline by ID"""
    return OrganizationPipeline.query.get(organization_pipeline_id)


def find_organization_pipeline_by_pipeline_run_uuid(pipeline_uuid):
    """ Fetch a OrganizationPipeline by pipeline uuid"""
    return OrganizationPipelineRun.query.filter(
        OrganizationPipelineRun.pipeline_run_uuid == pipeline_uuid
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


def find_organization_pipeline_run(organization_pipeline_id, uuid):
    """Find an Organization Pipeline Run
    NOTE: or used for backward compatibility.
    """
    return OrganizationPipelineRun.query.filter(
        and_(
            OrganizationPipelineRun.organization_pipeline_id
            == organization_pipeline_id,
            or_(
                OrganizationPipelineRun.pipeline_run_uuid == uuid,
                OrganizationPipelineRun.uuid == uuid,
            ),
        )
    ).one_or_none()


def find_latest_organization_pipeline_run(organization_pipeline_id):
    """Find the latest Organization Pipeline Run for an Organization Pipeline. """
    return (
        OrganizationPipelineRun.query.join(OrganizationPipeline)
        .filter(
            OrganizationPipelineRun.organization_pipeline_id
            == organization_pipeline_id,
            OrganizationPipeline.is_deleted == False,
        )
        .order_by(OrganizationPipelineRun.created_at.desc())
        .first()
    )


def search_organization_pipeline_runs(organization_pipeline_id, uuids):
    """Searches all Organization Pipeline Runs.
    NOTE: or used for backward compatibility.

    """
    return OrganizationPipelineRun.query.filter(
        and_(
            OrganizationPipelineRun.organization_pipeline_id
            == organization_pipeline_id,
            or_(
                OrganizationPipelineRun.pipeline_run_uuid.in_(uuids),
                OrganizationPipelineRun.uuid.in_(uuids),
            ),
        )
    ).all()
