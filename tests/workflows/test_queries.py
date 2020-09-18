from app.workflows import queries
from app import db
from app.workflows.models import Workflow, WorkflowPipeline, WorkflowPipelineDependency


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
    assert set(queries.find_workflows({"uuids": [w2.uuid, deleted_w.uuid]})) == set([w2])
    assert set(queries.find_workflows({"uuids": [w2.uuid, workflow.uuid]})) == set([workflow, w2])


def test_is_dag(app, workflow, pipeline):
    # A workflow with no edges when no edges are added is a digraph:
    assert queries.is_dag(workflow)

    pipeline_a = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    pipeline_b = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    pipeline_c = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    db.session.add(pipeline_a)
    db.session.add(pipeline_b)
    db.session.add(pipeline_c)
    a_to_b = WorkflowPipelineDependency(
        from_workflow_pipeline=pipeline_a,
        to_workflow_pipeline=pipeline_b,
    )
    b_to_c = WorkflowPipelineDependency(
        from_workflow_pipeline=pipeline_b,
        to_workflow_pipeline=pipeline_c,
    )
    db.session.add(a_to_b)
    db.session.add(b_to_c)
    db.session.commit()

    # Not adding any new edges succeeds
    assert queries.is_dag(workflow)

    # adding a non cycle does nothing.
    assert queries.is_dag(workflow, pipeline_a, pipeline_c)

    # trying to make a cycle fails
    assert not queries.is_dag(workflow, pipeline_c, pipeline_a)
