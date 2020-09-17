from .models import Workflow
from sqlalchemy import and_


def find_workflow(uuid):
    """ Find a workflow. """
    return Workflow.query.filter(
        and_(
            Workflow.uuid == uuid,
            Workflow.is_deleted == False,
        )
    ).one_or_none()
