from .models import Workflow, db
from .queries import find_workflow
from .schemas import CreateWorkflowSchema


def create_workflow(workflow_json):
    """ Create a Workflow. """
    data = CreateWorkflowSchema().load(workflow_json)

    workflow = Workflow(
        name=data["name"],
        description=data["description"],
    )
    db.session.add(workflow)
    db.session.commit()

    return workflow


def update_workflow(workflow_uuid, workflow_json):
    """ Update a Workflow. """
    workflow = find_workflow(workflow_uuid)
    if workflow is None:
        raise ValueError("no workflow found")

    data = CreateWorkflowSchema().load(workflow_json)

    workflow.name = data["name"]
    workflow.description = data["description"]
    db.session.commit()

    return workflow


def delete_workflow(workflow_uuid):
    """ Delete a workflow. """
    workflow = find_workflow(workflow_uuid)
    if workflow is None:
        raise ValueError("no workflow found")

    workflow.is_deleted = True
    db.session.commit()
