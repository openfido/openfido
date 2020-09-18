from .models import Workflow, WorkflowPipeline
from sqlalchemy import and_


def find_workflow(uuid):
    """ Find a workflow. """
    return Workflow.query.filter(
        and_(
            Workflow.uuid == uuid,
            Workflow.is_deleted == False,
        )
    ).one_or_none()


def find_workflows(uuids=None):
    """ Find all workflows, or a list of them. """
    query = Workflow.query.filter(Workflow.is_deleted == False)

    if uuids is not None:
        query = query.filter(Workflow.uuid.in_(uuids))

    return query


def find_workflow_pipeline(workflow_pipeline_uuid):
    """ Find a WorkflowPipeline. """
    return (
        WorkflowPipeline.query.join(Workflow)
        .filter(
            and_(
                WorkflowPipeline.uuid == workflow_pipeline_uuid,
                Workflow.is_deleted == False,
            )
        )
        .one_or_none()
    )
