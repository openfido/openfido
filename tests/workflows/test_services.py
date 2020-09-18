import pytest
from marshmallow.exceptions import ValidationError

from app.workflows import services
from app.workflows.queries import find_workflow


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


def test_update_workflow_bad_params(app, workflow):
    with pytest.raises(ValueError):
        services.update_workflow("no-id", {"name": "", "description": ""})
    with pytest.raises(ValidationError):
        services.update_workflow(workflow.uuid, {})
    with pytest.raises(ValidationError):
        services.update_workflow(workflow.uuid, {"name": "", "description": ""})


def test_update_workflow_bad_params(app, workflow):
    workflow = services.update_workflow(
        workflow.uuid, {"name": "updated workflow", "description": "update desc"}
    )
    assert workflow.uuid is not None
    assert workflow.name == "updated workflow"
    assert workflow.description == "update desc"


def test_delete_workflow_no_id(app):
    with pytest.raises(ValueError):
        services.delete_workflow("no-id")


def test_delete_workflow(app, workflow):
    the_uuid = workflow.uuid
    services.delete_workflow(the_uuid)
    assert find_workflow(the_uuid) is None


def test_create_workflow_pipeline(app, pipeline, workflow):
    # Creating a workflow pipeline with no sources/destinations is possible.
    workflow_pipeline = services.create_workflow_pipeline(workflow.uuid, {
        "pipeline_uuid": pipeline.uuid,
        "source_workflow_pipelines": [],
        "destination_workflow_pipelines": [],
    })
    assert workflow_pipeline.pipeline == pipeline
    assert workflow_pipeline.source_workflow_pipelines == []
    assert workflow_pipeline.dest_workflow_pipelines == []

    # Creating a workflow pipeline with a source
    source_workflow_pipeline = services.create_workflow_pipeline(workflow.uuid, {
        "pipeline_uuid": pipeline.uuid,
        "source_workflow_pipelines": [ workflow_pipeline.uuid ],
        "destination_workflow_pipelines": [],
    })
    assert source_workflow_pipeline.pipeline == pipeline
    assert len(source_workflow_pipeline.source_workflow_pipelines) == 0
    assert len(source_workflow_pipeline.dest_workflow_pipelines) == 1
    assert source_workflow_pipeline.dest_workflow_pipelines[0].from_workflow_pipeline == workflow_pipeline

    # Creating a workflow pipeline with a destination
    source_workflow_pipeline = services.create_workflow_pipeline(workflow.uuid, {
        "pipeline_uuid": pipeline.uuid,
        "source_workflow_pipelines": [],
        "destination_workflow_pipelines": [ workflow_pipeline.uuid ],
    })
    assert source_workflow_pipeline.pipeline == pipeline
    assert len(source_workflow_pipeline.source_workflow_pipelines) == 1
    assert len(source_workflow_pipeline.dest_workflow_pipelines) == 0
    assert source_workflow_pipeline.source_workflow_pipelines[0].to_workflow_pipeline == workflow_pipeline

    # Creating a workflow pipeline with a destination
    with_both_pipeline = services.create_workflow_pipeline(workflow.uuid, {
        "pipeline_uuid": pipeline.uuid,
        "source_workflow_pipelines": [ source_workflow_pipeline.uuid ],
        "destination_workflow_pipelines": [ workflow_pipeline.uuid ],
    })
    assert with_both_pipeline.pipeline == pipeline
    assert len(with_both_pipeline.source_workflow_pipelines) == 1
    assert len(with_both_pipeline.dest_workflow_pipelines) == 1
    assert with_both_pipeline.source_workflow_pipelines[0].to_workflow_pipeline == workflow_pipeline
    assert with_both_pipeline.dest_workflow_pipelines[0].from_workflow_pipeline == source_workflow_pipeline
