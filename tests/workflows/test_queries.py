from app.workflows import queries
from app import db


def test_find_workflow_bad_id(app):
    assert queries.find_workflow("no-id") is None


def test_find_workflow_is_deleted(app, workflow):
    workflow.is_deleted = True
    db.session.commit()

    assert queries.find_workflow(workflow.uuid) is None


def test_find_workflow(app, workflow):
    assert queries.find_workflow(workflow.uuid) == workflow
