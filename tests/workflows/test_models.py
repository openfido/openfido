from app.workflows.models import (
    db,
    Workflow,
    WorkflowPipeline,
    WorkflowPipelineDependency,
)


def test_workflow_pipeline(app, workflow):
    # a workflow initially has no pipelines
    assert len(workflow.workflow_pipelines) == 0


def test_workflow_pipeline(app, workflow_line, pipeline):
    pipeline_a = workflow_line.workflow_pipelines[0]
    pipeline_b = workflow_line.workflow_pipelines[1]
    pipeline_c = workflow_line.workflow_pipelines[2]
    a_to_b = pipeline_a.dest_workflow_pipelines[0]
    b_to_c = pipeline_b.dest_workflow_pipelines[0]

    assert set(pipeline_a.source_workflow_pipelines) == set([])
    assert set(pipeline_a.dest_workflow_pipelines) == set([a_to_b])
    assert set(pipeline_b.source_workflow_pipelines) == set([a_to_b])
    assert set(pipeline_b.dest_workflow_pipelines) == set([b_to_c])
    assert set(pipeline_c.source_workflow_pipelines) == set([b_to_c])
    assert set(pipeline_c.dest_workflow_pipelines) == set([])

    # the pipelines themselves can see all their associated workflow pipelines
    assert set(pipeline.workflow_pipelines) == set([pipeline_a, pipeline_b, pipeline_c])
