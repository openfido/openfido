import logging

from app.model_utils import RunStateEnum
from app.pipelines.queries import find_pipeline, find_run_state_type
from app.pipelines.schemas import CreateRunSchema
from app.pipelines.services import (
    copy_pipeline_run_artifact, create_pipeline_run, create_pipeline_run_state, start_pipeline_run,
    update_pipeline_run_state)

from .models import (
    Workflow, WorkflowPipeline, WorkflowPipelineDependency, WorkflowPipelineRun, WorkflowRun,
    WorkflowRunState, db)
from .queries import (
    find_dest_workflow_runs, find_source_workflow_runs, find_workflow, find_workflow_pipeline,
    is_dag, find_workflow_pipeline_dependency)
from .schemas import CreateWorkflowPipelineSchema, CreateWorkflowSchema

logger = logging.getLogger("workflow-services")


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


def _add_dependency(workflow_pipeline, another_workflow_pipeline_uuid, is_another_source):
    """ Add a WorkflowPipelineDependency to workflow_pipeline as a source or destination. """
    another_workflow_pipeline = find_workflow_pipeline(another_workflow_pipeline_uuid)

    if another_workflow_pipeline is None:
        db.session.rollback()
        raise ValueError(f"WorkflowPipeline {another_workflow_pipeline_uuid} not found")

    workflow = another_workflow_pipeline.workflow
    dag_args = [ workflow, another_workflow_pipeline, workflow_pipeline ]
    if is_another_source:
        dag_args = [ workflow, workflow_pipeline, another_workflow_pipeline ]

    if not is_dag(*dag_args):
        db.session.rollback()
        raise ValueError(
            f"Adding source_workflow_pipelines {another_workflow_pipeline_uuid} introduces a cycle."
        )

    wpd_qargs = {
        "from_workflow_pipeline": workflow_pipeline,
        "to_workflow_pipeline": another_workflow_pipeline,
    }
    if is_another_source:
        wpd_qargs = {
            "from_workflow_pipeline": another_workflow_pipeline,
            "to_workflow_pipeline": workflow_pipeline,
        }

    db.session.add(WorkflowPipelineDependency(**wpd_qargs))

def _remove_dependency(workflow_pipeline, another_workflow_pipeline_uuid, is_another_source):
    another_workflow_pipeline = find_workflow_pipeline(another_workflow_pipeline_uuid)

    if another_workflow_pipeline is None:
        raise ValueError(f"WorkflowPipeline {another_workflow_pipeline_uuid} not found")

    dependency = find_workflow_pipeline_dependency(workflow_pipeline, another_workflow_pipeline, is_another_source)

    if dependency is None:
        direction = "->" if is_another_source else "<-"
        raise ValueError(f"No dependency from {another_workflow_pipeline.uuid}->{workflow_pipeline.uuid}")

    db.session.delete(dependency)


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
        _add_dependency(workflow_pipeline, workflow_pipeline_uuid, True)

    for workflow_pipeline_uuid in data["destination_workflow_pipelines"]:
        _add_dependency(workflow_pipeline, workflow_pipeline_uuid, False)

    db.session.commit()

    return workflow_pipeline


def update_workflow_pipeline(workflow_uuid, workflow_pipeline_uuid, pipeline_json):
    workflow = find_workflow(workflow_uuid)
    if workflow is None:
        raise ValueError("no Workflow found")

    workflow_pipeline = find_workflow_pipeline(workflow_pipeline_uuid)
    if workflow_pipeline is None:
        raise ValueError("no WorkflowPipeline found")

    data = CreateWorkflowPipelineSchema().load(pipeline_json)

    pipeline = find_pipeline(data["pipeline_uuid"])
    if pipeline is None:
        raise ValueError(f"Pipeline {pipeline} not found")
    workflow_pipeline.pipeline = pipeline

    existing_sources = set([wp.from_workflow_pipeline.uuid for wp in workflow_pipeline.source_workflow_pipelines])
    new_sources = set(data["source_workflow_pipelines"])
    for new_workflow_pipeline_uuid in new_sources - existing_sources:
        _add_dependency(workflow_pipeline, new_workflow_pipeline_uuid, True)
    for new_workflow_pipeline_uuid in existing_sources - new_sources:
        _remove_dependency(workflow_pipeline, new_workflow_pipeline_uuid, True)

    existing_dests = set([wp.to_workflow_pipeline.uuid for wp in workflow_pipeline.dest_workflow_pipelines])
    new_dests = set(data["destination_workflow_pipelines"])
    for new_workflow_pipeline_uuid in new_dests - existing_dests:
        _add_dependency(workflow_pipeline, new_workflow_pipeline_uuid, False)
    for new_workflow_pipeline_uuid in existing_dests - new_dests:
        _remove_dependency(workflow_pipeline, new_workflow_pipeline_uuid, False)

    db.session.commit()

    return workflow_pipeline


def create_workflow_run_state(run_state_enum):
    run_state_type = find_run_state_type(run_state_enum)
    workflow_run_state = WorkflowRunState()
    run_state_type.workflow_run_states.append(workflow_run_state)

    return workflow_run_state


def update_workflow_run_state(workflow_run, run_state_enum):
    """Change the run state of a WorkflowRun.

    If the state is terminal (FAILED, ABORTED, COMPLETED) underlying
    WorkflowPipelineRun instances will be updated appropriately as well.
    """
    if workflow_run.run_state_enum() == run_state_enum:
        return

    if not workflow_run.run_state_enum().is_valid_transition(run_state_enum):
        raise ValueError(
            f"Invalid state transition: {workflow_run.run_state_enum().name}->{run_state_enum.name}"
        )

    workflow_run.workflow_run_states.append(create_workflow_run_state(run_state_enum))
    db.session.commit()
    return workflow_run


def create_workflow_run(workflow_uuid, run_json):
    """ Create a new WorkflowRun """
    data = CreateRunSchema().load(run_json)

    workflow = find_workflow(workflow_uuid)
    if workflow is None:
        raise ValueError("no workflow found")

    workflow_run = WorkflowRun(workflow=workflow)
    workflow_run.workflow_run_states.append(
        WorkflowRunState(run_state_type=find_run_state_type(RunStateEnum.NOT_STARTED))
    )

    added_run = False
    for workflow_pipeline in workflow.workflow_pipelines:
        if workflow_pipeline.is_deleted:
            continue
        queue_run = len(workflow_pipeline.source_workflow_pipelines) > 0
        no_input_data = {"callback_url": data["callback_url"], "inputs": []}
        run_data = no_input_data if queue_run else data
        pipeline_run = create_pipeline_run(
            workflow_pipeline.pipeline.uuid, run_data, queue_run
        )
        workflow_pipeline_run = WorkflowPipelineRun(
            workflow_run=workflow_run,
            pipeline_run=pipeline_run,
            workflow_pipeline=workflow_pipeline,
        )
        db.session.add(workflow_pipeline_run)
        added_run = True

    if not added_run:
        db.session.rollback()
        raise ValueError("No WorkflowPipelines exist!")

    db.session.add(workflow_run)
    db.session.commit()

    return workflow_run


def delete_workflow_pipeline(workflow_uuid, workflow_pipeline_uuid):
    """ Delete a WorkflowPipeline """
    workflow_pipeline = find_workflow_pipeline(workflow_pipeline_uuid)
    if workflow_pipeline is None:
        raise ValueError("no workflow_pipeline found")

    workflow_pipeline.is_deleted = True
    db.session.commit()


def update_workflow_run(pipeline_run):
    """If a pipeline_run is associated with a WorkflowPipelineRun, then update
    the WorkflowRun on state transitions.

    Returns updated WorkflowRun
    """
    if pipeline_run.workflow_pipeline_run is None:
        return None

    workflow_pipeline_run = pipeline_run.workflow_pipeline_run
    workflow_run = workflow_pipeline_run.workflow_run

    if pipeline_run.run_state_enum() == RunStateEnum.RUNNING:
        return update_workflow_run_state(workflow_run, RunStateEnum.RUNNING)

    if pipeline_run.run_state_enum() == RunStateEnum.FAILED:
        for wpr in workflow_run.workflow_pipeline_runs:
            if wpr.run_state_enum().in_final_state():
                continue

            update_pipeline_run_state(
                wpr.pipeline_run.uuid,
                {"state": RunStateEnum.ABORTED.name},
                apply_to_workflow_run=False,
            )

        return update_workflow_run_state(workflow_run, RunStateEnum.ABORTED)

    if pipeline_run.run_state_enum() != RunStateEnum.COMPLETED:
        error = f"Unexpected state encountered: {pipeline_run.run_state_enum()}"
        logger.warning(error)
        raise ValueError(error)

    # When a PipelineRun has COMPLETED we can continue the workflow:
    #  1. Pass its artifacts onward to any dest_workflow_pipelines
    #  2. Start new PipelineRuns for those pipelines.
    #  3. If there are none remaining, then this WorkflowRun is finished!

    for run in find_dest_workflow_runs(workflow_pipeline_run):
        for artifact in pipeline_run.pipeline_run_artifacts:
            copy_pipeline_run_artifact(artifact, run)

        sources = find_source_workflow_runs(run.workflow_pipeline_run)
        if set([s.run_state_enum() for s in sources]) == set([RunStateEnum.COMPLETED]):
            start_pipeline_run(run)

    run_states = [
        wpr.pipeline_run.run_state_enum() for wpr in workflow_run.workflow_pipeline_runs
    ]
    if set(run_states) == set([RunStateEnum.COMPLETED]):
        return update_workflow_run_state(workflow_run, RunStateEnum.COMPLETED)

    return workflow_run
