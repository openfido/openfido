from app.workflows.models import db, Workflow, WorkflowPipeline, WorkflowPipelineDependency

def test_workflow_pipeline(app, workflow, pipeline):
    # a workflow initially has no pipelines
    assert len(workflow.workflow_pipelines) == 0

    # pipelines can be made without any sources or destinations
    pipeline_a = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    pipeline_b = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    pipeline_c = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    db.session.add(pipeline_a)
    db.session.add(pipeline_b)
    db.session.add(pipeline_c)

    # pipelines can be updated to source and destinations
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

    assert set(pipeline_a.source_workflow_pipelines) == set([a_to_b])
    assert set(pipeline_a.dest_workflow_pipelines) == set([])
    assert set(pipeline_b.source_workflow_pipelines) == set([b_to_c])
    assert set(pipeline_b.dest_workflow_pipelines) == set([a_to_b])
    assert set(pipeline_c.source_workflow_pipelines) == set([])
    assert set(pipeline_c.dest_workflow_pipelines) == set([b_to_c])

    # the pipelines themselves can see all their associated workflow pipelines
    assert set(pipeline.workflow_pipelines) == set([pipeline_a, pipeline_b, pipeline_c])
