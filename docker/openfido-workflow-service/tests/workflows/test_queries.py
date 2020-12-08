from unittest.mock import patch

from app import db
from app.pipelines.models import Pipeline
from app.workflows import queries
from app.workflows.models import Workflow, WorkflowPipeline, WorkflowPipelineDependency
from app.workflows.services import create_workflow_run, delete_workflow_pipeline


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
    w2 = Workflow(
        name="workflow 2",
        description="description 2",
    )
    deleted_w = Workflow(
        name="a workflow", description="a description", is_deleted=True
    )
    db.session.add(w2)
    db.session.add(deleted_w)
    db.session.commit()

    assert set(queries.find_workflows()) == set([workflow, w2])
    assert set(queries.find_workflows({"uuids": [w2.uuid, deleted_w.uuid]})) == set(
        [w2]
    )
    assert set(queries.find_workflows({"uuids": [w2.uuid, workflow.uuid]})) == set(
        [workflow, w2]
    )


def test_is_dag(app, workflow_line, pipeline):
    # Not adding any new edges succeeds
    # assert queries.is_dag(workflow_line)

    # adding a non cycle does nothing.
    [a, b, c] = workflow_line.workflow_pipelines
    assert queries.is_dag(workflow_line, a, c)

    # trying to make a cycle fails
    assert not queries.is_dag(workflow_line, c, a)


def test_pipeline_has_workflow_pipeline(app, workflow, pipeline, workflow_pipeline):
    assert queries.pipeline_has_workflow_pipeline(pipeline.id)

    p1 = Pipeline(
        name="pipeline 1",
        description="a description",
        docker_image_url="",
        repository_ssh_url="",
        repository_branch="",
    )
    db.session.add(p1)
    db.session.commit()

    assert not queries.pipeline_has_workflow_pipeline(p1.id)


@patch("app.pipelines.services.execute_pipeline.delay")
def test_find_dest_workflow_runs(delay_mock, app, workflow_line):
    workflow_run = create_workflow_run(
        workflow_line.uuid,
        {
            "callback_url": "http://example.com/cb",
            "inputs": [],
        },
    )
    assert queries.find_dest_workflow_runs(workflow_run.workflow_pipeline_runs[0]) == [
        workflow_run.workflow_pipeline_runs[1].pipeline_run
    ]
    assert queries.find_dest_workflow_runs(workflow_run.workflow_pipeline_runs[1]) == [
        workflow_run.workflow_pipeline_runs[2].pipeline_run
    ]
    assert queries.find_dest_workflow_runs(workflow_run.workflow_pipeline_runs[2]) == []

    # if a workflow_pipeline is deleted it is not found/included
    delete_workflow_pipeline(
        workflow_run.workflow.uuid,
        workflow_run.workflow_pipeline_runs[1].workflow_pipeline.uuid,
    )
    assert queries.find_dest_workflow_runs(workflow_run.workflow_pipeline_runs[0]) == []


@patch("app.pipelines.services.execute_pipeline.delay")
def test_find_source_workflow_runs(delay_mock, app, workflow_line):
    workflow_run = create_workflow_run(
        workflow_line.uuid,
        {
            "callback_url": "http://example.com/cb",
            "inputs": [],
        },
    )
    assert (
        queries.find_source_workflow_runs(workflow_run.workflow_pipeline_runs[0]) == []
    )
    assert queries.find_source_workflow_runs(
        workflow_run.workflow_pipeline_runs[1]
    ) == [workflow_run.workflow_pipeline_runs[0].pipeline_run]
    assert queries.find_source_workflow_runs(
        workflow_run.workflow_pipeline_runs[2]
    ) == [workflow_run.workflow_pipeline_runs[1].pipeline_run]

    # if a workflow_pipeline is deleted it is not found/included
    delete_workflow_pipeline(
        workflow_run.workflow.uuid,
        workflow_run.workflow_pipeline_runs[1].workflow_pipeline.uuid,
    )
    assert (
        queries.find_source_workflow_runs(workflow_run.workflow_pipeline_runs[2]) == []
    )
