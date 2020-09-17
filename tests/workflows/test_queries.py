from app.workflows import queries
from app import db
from app.workflows.models import Workflow


def test_find_workflow_bad_id(app):
    assert queries.find_workflow("no-id") is None


def test_find_workflow_is_deleted(app, workflow):
    workflow.is_deleted = True
    db.session.commit()

    assert queries.find_workflow(workflow.uuid) is None


def test_find_workflow(app, workflow):
    assert queries.find_workflow(workflow.uuid) == workflow


def test_find_workflows_no_workflows(app):
    assert list(queries.find_workflows()) == []


def test_find_workflows(app, workflow):
    p2 = Workflow(
        name="workflow 2",
        description="description 2",
    )
    deleted_p = Workflow(
        name="a workflow", description="a description", is_deleted=True
    )
    db.session.add(p2)
    db.session.add(deleted_p)
    db.session.commit()

    assert set(queries.find_workflows()) == set([workflow, p2])
    assert set(queries.find_workflows([p2.uuid, deleted_p.uuid])) == set([p2])
    assert set(queries.find_workflows([p2.uuid, workflow.uuid])) == set([workflow, p2])
