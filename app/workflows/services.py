from app.pipelines.queries import find_pipeline

from .models import Workflow, db, WorkflowPipeline, WorkflowPipelineDependency
from .queries import find_workflow, find_workflow_pipeline
from .schemas import CreateWorkflowSchema, CreateWorkflowPipelineSchema


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

    # TODO detect DAG

    workflow_pipeline = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    db.session.add(workflow_pipeline)

    for workflow_pipeline_uuid in data["source_workflow_pipelines"]:
        source_workflow_pipeline = find_workflow_pipeline(workflow_pipeline_uuid)
        if source_workflow_pipeline is None:
            db.session.rollback()
            raise ValueError(f"WorkflowPipeline {workflow_pipeline_uuid} not found")

        source_to_wp = WorkflowPipelineDependency(
            to_workflow_pipeline=source_workflow_pipeline,
            from_workflow_pipeline=workflow_pipeline,
        )
        db.session.add(source_to_wp)

    for workflow_pipeline_uuid in data["destination_workflow_pipelines"]:
        dest_workflow_pipeline = find_workflow_pipeline(workflow_pipeline_uuid)
        if dest_workflow_pipeline is None:
            db.session.rollback()
            raise ValueError(f"WorkflowPipeline {workflow_pipeline_uuid} not found")

        wp_to_dest = WorkflowPipelineDependency(
            to_workflow_pipeline=workflow_pipeline,
            from_workflow_pipeline=dest_workflow_pipeline,
        )
        db.session.add(wp_to_dest)

    db.session.commit()

    return workflow_pipeline
