from unittest.mock import patch, call

import pytest
from app import db
from app.model_utils import RunStateEnum
from app.pipelines.models import PipelineRunArtifact
from app.pipelines.services import create_pipeline_run, create_pipeline_run_state
from app.workflows import services
from app.workflows.models import WorkflowPipeline
from app.workflows.queries import find_workflow
from app.workflows.services import (
    create_workflow_pipeline,
    create_workflow_pipeline_run,
    create_workflow_run_state,
    update_workflow_run,
)
from marshmallow.exceptions import ValidationError

from ..pipelines.test_services import VALID_CALLBACK_INPUT


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


def test_create_workflow_pipeline_no_workflow(app):
    with pytest.raises(ValueError):
        workflow_pipeline = services.create_workflow_pipeline(
            "no-id",
            {
                "pipeline_uuid": "no-id",
                "source_workflow_pipelines": [],
                "destination_workflow_pipelines": [],
            },
        )


def test_create_workflow_pipeline_no_pipeline(app, workflow):
    with pytest.raises(ValueError):
        workflow_pipeline = services.create_workflow_pipeline(
            workflow.uuid,
            {
                "pipeline_uuid": "a" * 32,
                "source_workflow_pipelines": [],
                "destination_workflow_pipelines": [],
            },
        )


def test_create_workflow_pipeline_no_source(app, pipeline, workflow):
    with pytest.raises(ValueError):
        services.create_workflow_pipeline(
            workflow.uuid,
            {
                "pipeline_uuid": pipeline.uuid,
                "source_workflow_pipelines": ["a" * 32],
                "destination_workflow_pipelines": [],
            },
        )
    assert (
        WorkflowPipeline.query.filter(
            WorkflowPipeline.pipeline == pipeline
        ).one_or_none()
        is None
    )


def test_create_workflow_pipeline_no_dest(app, pipeline, workflow):
    with pytest.raises(ValueError):
        services.create_workflow_pipeline(
            workflow.uuid,
            {
                "pipeline_uuid": pipeline.uuid,
                "source_workflow_pipelines": [],
                "destination_workflow_pipelines": ["a" * 32],
            },
        )
    assert (
        WorkflowPipeline.query.filter(
            WorkflowPipeline.pipeline == pipeline
        ).one_or_none()
        is None
    )


@patch("app.workflows.services.is_dag")
def test_create_workflow_pipeline_from_cycle(is_dag_mock, app, pipeline, workflow):
    is_dag_mock.return_value = False

    workflow_pipeline = services.create_workflow_pipeline(
        workflow.uuid,
        {
            "pipeline_uuid": pipeline.uuid,
            "source_workflow_pipelines": [],
            "destination_workflow_pipelines": [],
        },
    )

    with pytest.raises(ValueError):
        services.create_workflow_pipeline(
            workflow.uuid,
            {
                "pipeline_uuid": pipeline.uuid,
                "source_workflow_pipelines": [workflow_pipeline.uuid],
                "destination_workflow_pipelines": [],
            },
        )

    with pytest.raises(ValueError):
        services.create_workflow_pipeline(
            workflow.uuid,
            {
                "pipeline_uuid": pipeline.uuid,
                "source_workflow_pipelines": [],
                "destination_workflow_pipelines": [workflow_pipeline.uuid],
            },
        )


def test_create_workflow_pipeline(app, pipeline, workflow):
    # Creating a workflow pipeline with no sources/destinations is possible.
    workflow_pipeline = services.create_workflow_pipeline(
        workflow.uuid,
        {
            "pipeline_uuid": pipeline.uuid,
            "source_workflow_pipelines": [],
            "destination_workflow_pipelines": [],
        },
    )
    assert workflow_pipeline.pipeline == pipeline
    assert workflow_pipeline.source_workflow_pipelines == []
    assert workflow_pipeline.dest_workflow_pipelines == []

    # Creating a workflow pipeline with a source
    source_workflow_pipeline = services.create_workflow_pipeline(
        workflow.uuid,
        {
            "pipeline_uuid": pipeline.uuid,
            "source_workflow_pipelines": [workflow_pipeline.uuid],
            "destination_workflow_pipelines": [],
        },
    )
    assert source_workflow_pipeline.pipeline == pipeline
    assert len(source_workflow_pipeline.source_workflow_pipelines) == 1
    assert len(source_workflow_pipeline.dest_workflow_pipelines) == 0
    assert (
        source_workflow_pipeline.source_workflow_pipelines[0].from_workflow_pipeline
        == workflow_pipeline
    )
    assert (
        source_workflow_pipeline.source_workflow_pipelines[0].to_workflow_pipeline
        == source_workflow_pipeline
    )

    # Creating a workflow pipeline with a destination
    source_workflow_pipeline = services.create_workflow_pipeline(
        workflow.uuid,
        {
            "pipeline_uuid": pipeline.uuid,
            "source_workflow_pipelines": [],
            "destination_workflow_pipelines": [workflow_pipeline.uuid],
        },
    )
    assert source_workflow_pipeline.pipeline == pipeline
    assert len(source_workflow_pipeline.source_workflow_pipelines) == 0
    assert len(source_workflow_pipeline.dest_workflow_pipelines) == 1
    assert (
        source_workflow_pipeline.dest_workflow_pipelines[0].from_workflow_pipeline
        == source_workflow_pipeline
    )
    assert (
        source_workflow_pipeline.dest_workflow_pipelines[0].to_workflow_pipeline
        == workflow_pipeline
    )

    # Creating a workflow pipeline with a destination
    with_both_pipeline = services.create_workflow_pipeline(
        workflow.uuid,
        {
            "pipeline_uuid": pipeline.uuid,
            "source_workflow_pipelines": [source_workflow_pipeline.uuid],
            "destination_workflow_pipelines": [workflow_pipeline.uuid],
        },
    )
    assert with_both_pipeline.pipeline == pipeline
    assert len(with_both_pipeline.source_workflow_pipelines) == 1
    assert len(with_both_pipeline.dest_workflow_pipelines) == 1
    assert (
        with_both_pipeline.source_workflow_pipelines[0].from_workflow_pipeline
        == source_workflow_pipeline
    )
    assert (
        with_both_pipeline.source_workflow_pipelines[0].to_workflow_pipeline
        == with_both_pipeline
    )
    assert (
        with_both_pipeline.dest_workflow_pipelines[0].from_workflow_pipeline
        == with_both_pipeline
    )
    assert (
        with_both_pipeline.dest_workflow_pipelines[0].to_workflow_pipeline
        == workflow_pipeline
    )


def test_create_workflow_pipeline_run_no_workflow(app, pipeline, workflow):
    with pytest.raises(ValueError):
        services.create_workflow_pipeline_run(
            "no-id", {"callback_url": "https://example.com", "inputs": []}
        )


def test_create_workflow_pipeline_run(app, pipeline, workflow_pipeline):
    create_data = {
        "callback_url": "https://example.com",
        "inputs": [
            {
                "name": "aname.pdf",
                "url": "https://example.com/ex.pdf",
            }
        ],
    }
    # A new WorkflowPipelineRun creates new PipelineRuns as QUEUED...when the
    # celery worker runs it'll update their states appropriately.
    workflow_pipeline_run = services.create_workflow_pipeline_run(
        workflow_pipeline.workflow.uuid, create_data
    )
    assert len(workflow_pipeline_run.workflow_run_states) == 1
    assert (
        workflow_pipeline_run.workflow_run_states[0].run_state_type.code
        == RunStateEnum.NOT_STARTED
    )
    assert len(workflow_pipeline_run.workflow_pipeline_runs) == 1
    pipeline_run = workflow_pipeline_run.workflow_pipeline_runs[0].pipeline_run
    assert pipeline_run.callback_url == create_data["callback_url"]
    assert len(pipeline_run.pipeline_run_states) == 1
    assert pipeline_run.pipeline_run_states[0].code == RunStateEnum.QUEUED
    assert len(pipeline_run.pipeline_run_inputs) == 1
    assert (
        pipeline_run.pipeline_run_inputs[0].filename == create_data["inputs"][0]["name"]
    )
    assert pipeline_run.pipeline_run_inputs[0].url == create_data["inputs"][0]["url"]


@patch("app.pipelines.services.execute_pipeline")
def test_update_workflow_run_no_workflow(execute_pipeline_mock, app, pipeline):
    # a pipeline_run not associated with workflow_pipeline_run nothing breaks
    pipeline_run = create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)
    assert update_workflow_run(pipeline_run) is None


def _configure_run_state(workflow, run_state_enum):
    """ Update first PipelineRun to run_state_enum and call update_workflow_run() """
    create_workflow_pipeline_run(
        workflow.uuid,
        {
            "callback_url": "http://example.com/cb",
            "inputs": [],
        },
    )
    pipeline_runs = [
        wpr.pipeline_run for wpr in workflow.workflow_runs[0].workflow_pipeline_runs
    ]
    pipeline_runs[0].pipeline_run_states.append(
        create_pipeline_run_state(run_state_enum)
    )
    pipeline_runs[0].pipeline_run_artifacts.append(
        PipelineRunArtifact(name="afile.txt")
    )
    db.session.commit()

    return (update_workflow_run(pipeline_runs[0]), pipeline_runs)


@patch("app.pipelines.services.execute_pipeline")
def test_update_workflow_run_QUEUE(
    execute_pipeline_mock, app, pipeline, workflow_line
):
    # when a PipelineRun gives some unexpected state, an error is thrown
    with pytest.raises(ValueError):
        (workflow_run, pipeline_runs) = _configure_run_state(
            workflow_line, RunStateEnum.QUEUED
        )


@patch("app.pipelines.services.execute_pipeline")
def test_update_workflow_run_FAILED(
    execute_pipeline_mock, app, pipeline, workflow_line
):
    # when a PipelineRun fails, then all the remaining PRs should be marked as
    # ABORTED -- and the WorkflowRun itself should be FAILED.
    (workflow_run, pipeline_runs) = _configure_run_state(
        workflow_line, RunStateEnum.FAILED
    )

    assert workflow_run.run_state_enum() == RunStateEnum.FAILED
    assert pipeline_runs[1].run_state_enum() == RunStateEnum.ABORTED
    assert pipeline_runs[2].run_state_enum() == RunStateEnum.ABORTED
    assert not execute_pipeline_mock.called


@patch("app.pipelines.services.execute_pipeline")
def test_update_workflow_run_RUNNING(
    execute_pipeline_mock, app, pipeline, workflow_line
):
    (workflow_run, pipeline_runs) = _configure_run_state(
        workflow_line, RunStateEnum.RUNNING
    )

    assert workflow_run.run_state_enum() == RunStateEnum.RUNNING
    assert pipeline_runs[1].run_state_enum() == RunStateEnum.QUEUED
    assert pipeline_runs[2].run_state_enum() == RunStateEnum.QUEUED
    assert not execute_pipeline_mock.called


@patch("app.workflows.services.copy_pipeline_run_artifact")
@patch("app.pipelines.services.execute_pipeline.delay")
def test_update_workflow_run_RUNNING_line(delay_mock, copy_mock, app, pipeline, workflow_line):
    (workflow_run, pipeline_runs) = _configure_run_state(
        workflow_line, RunStateEnum.COMPLETED
    )
    workflow_run.workflow_run_states.append(
        create_workflow_run_state(RunStateEnum.RUNNING)
    )

    assert workflow_run.run_state_enum() == RunStateEnum.RUNNING
    copy_mock.assert_called_once_with(pipeline_runs[0].pipeline_run_artifacts[0], pipeline_runs[1])
    assert pipeline_runs[1].run_state_enum() == RunStateEnum.NOT_STARTED
    assert pipeline_runs[2].run_state_enum() == RunStateEnum.QUEUED
    delay_mock.assert_called_once()

    # when the second run finished it'll start the last one
    delay_mock.reset_mock()
    copy_mock.reset_mock()
    pipeline_runs[1].pipeline_run_artifacts.append(PipelineRunArtifact(name="anotherfile.txt"))
    pipeline_runs[1].pipeline_run_states.append(
        create_pipeline_run_state(RunStateEnum.COMPLETED)
    )
    update_workflow_run(pipeline_runs[1])
    assert workflow_run.run_state_enum() == RunStateEnum.RUNNING
    copy_mock.assert_called_once_with(pipeline_runs[1].pipeline_run_artifacts[0], pipeline_runs[2])
    assert pipeline_runs[2].run_state_enum() == RunStateEnum.NOT_STARTED

    # Finally, when the last run finishes, the workflow is finished
    delay_mock.reset_mock()
    copy_mock.reset_mock()
    pipeline_runs[2].pipeline_run_states.append(
        create_pipeline_run_state(RunStateEnum.COMPLETED)
    )
    update_workflow_run(pipeline_runs[2])
    assert workflow_run.run_state_enum() == RunStateEnum.COMPLETED
    assert not copy_mock.called


@patch("app.workflows.services.copy_pipeline_run_artifact")
@patch("app.pipelines.services.execute_pipeline.delay")
def test_update_workflow_run_RUNNING_square(delay_mock, copy_mock, app, pipeline, workflow_square):
    (workflow_run, pipeline_runs) = _configure_run_state(
        workflow_square, RunStateEnum.COMPLETED
    )
    workflow_run.workflow_run_states.append(
        create_workflow_run_state(RunStateEnum.RUNNING)
    )

    assert workflow_run.run_state_enum() == RunStateEnum.RUNNING
    copy_mock.assert_has_calls([
        call(pipeline_runs[0].pipeline_run_artifacts[0], pipeline_runs[1]),
        call(pipeline_runs[0].pipeline_run_artifacts[0], pipeline_runs[2]),
    ])
    assert pipeline_runs[1].run_state_enum() == RunStateEnum.NOT_STARTED
    assert pipeline_runs[2].run_state_enum() == RunStateEnum.NOT_STARTED
    assert pipeline_runs[3].run_state_enum() == RunStateEnum.QUEUED
    assert delay_mock.call_count == 2

    # when one of the second ones finishes - the third one gets its artifact,
    # but it doesn't start (b/c it needs artifacts from both!)
    delay_mock.reset_mock()
    copy_mock.reset_mock()
    pipeline_runs[1].pipeline_run_artifacts.append(PipelineRunArtifact(name="anotherfile.txt"))
    pipeline_runs[1].pipeline_run_states.append(create_pipeline_run_state(RunStateEnum.COMPLETED))
    update_workflow_run(pipeline_runs[1])
    assert workflow_run.run_state_enum() == RunStateEnum.RUNNING
    copy_mock.assert_called_once_with(pipeline_runs[1].pipeline_run_artifacts[0], pipeline_runs[3])
    assert pipeline_runs[3].run_state_enum() == RunStateEnum.QUEUED

    # when the third one finishes - the fourth starts b/c it has all its inputs
    delay_mock.reset_mock()
    copy_mock.reset_mock()
    pipeline_runs[2].pipeline_run_artifacts.append(PipelineRunArtifact(name="anotherfile.txt"))
    pipeline_runs[2].pipeline_run_states.append(create_pipeline_run_state(RunStateEnum.COMPLETED))
    update_workflow_run(pipeline_runs[2])
    assert workflow_run.run_state_enum() == RunStateEnum.RUNNING
    copy_mock.assert_called_once_with(pipeline_runs[2].pipeline_run_artifacts[0], pipeline_runs[3])
    assert pipeline_runs[3].run_state_enum() == RunStateEnum.NOT_STARTED

    # Finally, when the last run finishes, the workflow is finished
    delay_mock.reset_mock()
    copy_mock.reset_mock()
    pipeline_runs[3].pipeline_run_states.append(
        create_pipeline_run_state(RunStateEnum.COMPLETED)
    )
    update_workflow_run(pipeline_runs[3])
    assert workflow_run.run_state_enum() == RunStateEnum.COMPLETED
    assert not copy_mock.called
