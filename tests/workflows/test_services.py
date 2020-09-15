import pytest
from marshmallow.exceptions import ValidationError

from app.workflows import services


def test_create_workflow_bad_params(app):
    with pytest.raises(ValidationError):
        services.create_workflow(None)
    with pytest.raises(ValidationError):
        services.create_workflow({})
    with pytest.raises(ValidationError):
        services.create_workflow({"name": "", "description": ""})


def test_create_workflow_bad_params(app):
    workflow = services.create_workflow({"name": "a workflow", "description": "desc"})
    assert workflow.uuid is not None
    assert workflow.name == "a workflow"
    assert workflow.description == "desc"
