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
                Workflow.is_deleted == False,
            )
        )
        .one_or_none()
    )


def find_workflow_pipeline_dependencies(workflow_uuid):
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


def find_workflow_pipelines(workflow_uuid):
    """ Find all workflow pipelines, or a list of them. """
    return WorkflowPipeline.query.filter(Workflow.workflow_id == workflow_uuid)


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
