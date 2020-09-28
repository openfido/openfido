from sqlalchemy import and_, or_

import networkx as nx

from .models import (
    db,
    Workflow,
    WorkflowPipeline,
    WorkflowPipelineDependency,
    WorkflowRun,
)
from .schemas import SearchWorkflowsSchema


def find_workflow(uuid):
    """ Find a workflow. """
    return Workflow.query.filter(
        and_(
            Workflow.uuid == uuid,
            Workflow.is_deleted == False,
        )
    ).one_or_none()


def find_workflows(uuids=None):
    """ Find all workflows, or a list of them. """
    query = Workflow.query.filter(Workflow.is_deleted == False)

    if uuids is not None:
        data = SearchWorkflowsSchema().load(uuids)
        query = query.filter(Workflow.uuid.in_(map(str, data["uuids"])))

    return query


def find_workflow_pipeline(workflow_pipeline_uuid):
    """ Find a WorkflowPipeline. """
    return (
        WorkflowPipeline.query.join(Workflow)
        .filter(
            and_(
                WorkflowPipeline.uuid == workflow_pipeline_uuid,
                WorkflowPipeline.is_deleted == False,
                Workflow.is_deleted == False,
            )
        )
        .one_or_none()
    )


def find_workflow_pipeline_dependencies(workflow_uuid):
    """ Return all WorkflowPipelineDependency for a Workflow. """
    workflow_pipeline_sq = (
        db.session.query(WorkflowPipeline.id)
        .join(Workflow)
        .filter(
            Workflow.is_deleted == False,
            Workflow.uuid == workflow_uuid,
        )
        .subquery("workflow_pipeline_sq")
    )
    return WorkflowPipelineDependency.query.filter(
        or_(
            WorkflowPipelineDependency.from_workflow_pipeline_id.in_(
                workflow_pipeline_sq
            ),
            WorkflowPipelineDependency.to_workflow_pipeline_id.in_(
                workflow_pipeline_sq
            ),
        )
    )


def find_workflow_pipeline_dependency(workflow_pipeline, another_pipeline, is_another_source):
    from_wp = workflow_pipeline
    to_wp = another_pipeline
    if is_another_source:
        from_wp = another_pipeline
        to_wp = workflow_pipeline

    return WorkflowPipelineDependency.query.filter(
        WorkflowPipelineDependency.from_workflow_pipeline == from_wp,
        WorkflowPipelineDependency.to_workflow_pipeline == to_wp,
    ).one_or_none()


def is_dag(workflow, from_workflow_pipeline=None, to_workflow_pipeline=None):
    """Returns True if the graph supplied a directed acyclic graph and adding a
    new edge would not introduce a cycle."""

    dependencies = find_workflow_pipeline_dependencies(workflow.uuid)
    digraph = nx.DiGraph()
    for dependency in dependencies:
        digraph.add_edge(
            dependency.from_workflow_pipeline_id, dependency.to_workflow_pipeline_id
        )

    if from_workflow_pipeline is not None and to_workflow_pipeline is not None:
        digraph.add_edge(from_workflow_pipeline.id, to_workflow_pipeline.id)

    return nx.is_directed_acyclic_graph(digraph)


def find_dest_workflow_runs(workflow_pipeline_run):
    """Find all PipelineRuns.dest_workflow_pipelines of a WorkflowPipelineRun"""
    workflow_run = workflow_pipeline_run.workflow_run
    result = []
    for dest_wp in workflow_pipeline_run.workflow_pipeline.dest_workflow_pipelines:
        if dest_wp.to_workflow_pipeline.is_deleted:
            continue
        result.extend(
            [
                wpr.pipeline_run
                for wpr in dest_wp.to_workflow_pipeline.workflow_pipeline_runs
                if wpr.workflow_run == workflow_run
            ]
        )
    return result


def find_source_workflow_runs(workflow_pipeline_run):
    """Find all PipelineRuns.source_workflow_pipelines of a WorkflowPipelineRun"""
    workflow_run = workflow_pipeline_run.workflow_run
    result = []
    for dest_wp in workflow_pipeline_run.workflow_pipeline.source_workflow_pipelines:
        if dest_wp.from_workflow_pipeline.is_deleted:
            continue
        result.extend(
            [
                wpr.pipeline_run
                for wpr in dest_wp.from_workflow_pipeline.workflow_pipeline_runs
                if wpr.workflow_run == workflow_run
            ]
        )
    return result


def pipeline_has_workflow_pipeline(pipeline_id):
    """ Find a WorkflowPipeline by pipeline ID. """
    return (
        WorkflowPipeline.query.join(Workflow)
        .filter(
            and_(
                WorkflowPipeline.pipeline_id == pipeline_id,
                Workflow.is_deleted == False,
            )
        )
        .scalar()
    ) is not None


def find_workflow_run(workflow_run_uuid):
    """ Find a WorkflowRun. """
    return (
        WorkflowRun.query.join(Workflow)
        .filter(
            and_(
                WorkflowRun.uuid == workflow_run_uuid,
                Workflow.is_deleted == False,
            )
        )
        .one_or_none()
    )
