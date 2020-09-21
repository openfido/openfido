from app.model_utils import RunStateEnum
from app.pipelines.queries import find_pipeline, find_run_state_type
from app.pipelines.schemas import CreateRunSchema
from app.pipelines.services import create_pipeline_run_state, create_queued_pipeline_run

from .models import (
    Workflow,
    WorkflowPipeline,
    WorkflowPipelineDependency,
    WorkflowPipelineRun,
    WorkflowRun,
    WorkflowRunState,
    db,
)
from .queries import find_workflow, find_workflow_pipeline, is_dag
from .schemas import CreateWorkflowPipelineSchema, CreateWorkflowSchema


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


def create_workflow_pipeline(workflow_uuid, pipeline_json):
    """ Create a WorkflowPipeline """
    workflow = find_workflow(workflow_uuid)
    if workflow is None:
        raise ValueError("no workflow found")

    data = CreateWorkflowPipelineSchema().load(pipeline_json)

    pipeline = find_pipeline(data["pipeline_uuid"])
    if pipeline is None:
        raise ValueError(f"Pipeline {pipeline} not found")

    workflow_pipeline = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    db.session.add(workflow_pipeline)

    for workflow_pipeline_uuid in data["source_workflow_pipelines"]:
        source_workflow_pipeline = find_workflow_pipeline(workflow_pipeline_uuid)
        if source_workflow_pipeline is None:
            db.session.rollback()
            raise ValueError(f"WorkflowPipeline {workflow_pipeline_uuid} not found")

        if not is_dag(workflow, workflow_pipeline, source_workflow_pipeline):
            db.session.rollback()
            raise ValueError(
                f"Adding source_workflow_pipelines {workflow_pipeline_uuid} introduces a cycle."
            )

        source_to_wp = WorkflowPipelineDependency(
            from_workflow_pipeline=workflow_pipeline,
            to_workflow_pipeline=source_workflow_pipeline,
        )
        db.session.add(source_to_wp)

    for workflow_pipeline_uuid in data["destination_workflow_pipelines"]:
        dest_workflow_pipeline = find_workflow_pipeline(workflow_pipeline_uuid)
        if dest_workflow_pipeline is None:
            db.session.rollback()
            raise ValueError(f"WorkflowPipeline {workflow_pipeline_uuid} not found")

        if not is_dag(workflow, workflow_pipeline, dest_workflow_pipeline):
            db.session.rollback()
            raise ValueError(
                f"Adding dest_workflow_pipelines {workflow_pipeline_uuid} introduces a cycle."
            )

        wp_to_dest = WorkflowPipelineDependency(
            to_workflow_pipeline=workflow_pipeline,
            from_workflow_pipeline=dest_workflow_pipeline,
        )
        db.session.add(wp_to_dest)

    db.session.commit()

    return workflow_pipeline


def create_workflow_pipeline_run(workflow_uuid, run_json):
    """ Create a new workflow pipeline run """
    data = CreateRunSchema().load(run_json)

    workflow = find_workflow(workflow_uuid)
    if workflow is None:
        raise ValueError("no workflow found")

    workflow_run = WorkflowRun(workflow=workflow)
    workflow_run.workflow_run_states.append(
        WorkflowRunState(run_state_type=find_run_state_type(RunStateEnum.NOT_STARTED))
    )

    for workflow_pipeline in workflow.workflow_pipelines:
        pipeline_run = create_queued_pipeline_run(workflow_pipeline.pipeline.uuid, data)
        workflow_pipeline_run = WorkflowPipelineRun(
            workflow_run=workflow_run, pipeline_run=pipeline_run
        )
        db.session.add(workflow_pipeline_run)

    # TODO start a new celery worker task

    db.session.add(workflow_run)

    db.session.commit()

    return workflow_run


def delete_workflow_pipeline(workflow_uuid, workflow_pipeline_uuid):
    """ Delete a WorkflowPipeline """
    workflow_pipeline = find_workflow_pipeline(workflow_pipeline_uuid)
    if workflow_pipeline is None:
        raise ValueError("no workflow_pipeline found")

    db.session.delete(workflow_pipeline)
    db.session.commit()
