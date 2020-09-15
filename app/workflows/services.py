from .schemas import CreateWorkflowSchema
from .models import db, Workflow


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
