from ..model_utils import CommonColumnsMixin, get_db

db = get_db()


class Workflow(CommonColumnsMixin, db.Model):
    """ A collection of connected pipelines and runs. """

    __tablename__ = "workflow"

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)

    workflow_pipelines = db.relationship(
        "WorkflowPipeline", backref="workflow", lazy="select"
    )
    workflow_runs = db.relationship("WorkflowRun", backref="workflow", lazy="select")


class WorkflowPipeline(CommonColumnsMixin, db.Model):
    """ A pipeline that is part of a workflow. """

    __tablename__ = "workflowpipeline"

    pipeline_id = db.Column(db.Integer, db.ForeignKey("pipeline.id"), nullable=False)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflow.id"), nullable=False)

    source_workflow_pipelines = db.relationship(
        "WorkflowPipelineDependency",
        backref="from_workflow_pipeline",
        lazy="select",
        foreign_keys="[WorkflowPipelineDependency.from_workflow_pipeline_id]",
    )

    dest_workflow_pipelines = db.relationship(
        "WorkflowPipelineDependency",
        backref="to_workflow_pipeline",
        lazy="select",
        foreign_keys="[WorkflowPipelineDependency.to_workflow_pipeline_id]",
    )

    workflow_pipeline_runs = db.relationship(
        "WorkflowPipelineRun",
        backref="workflow_pipeline",
        lazy="select",
    )


class WorkflowPipelineDependency(CommonColumnsMixin, db.Model):
    """ A dependency between pipelines. """

    __tablename__ = "workflowpipelinedependency"

    from_workflow_pipeline_id = db.Column(
        db.Integer, db.ForeignKey("workflowpipeline.id"), nullable=False
    )

    to_workflow_pipeline_id = db.Column(
        db.Integer, db.ForeignKey("workflowpipeline.id"), nullable=False
    )


class WorkflowRun(CommonColumnsMixin, db.Model):
    """ An execution of a Workflow. """

    __tablename__ = "workflowrun"

    workflow_id = db.Column(db.Integer, db.ForeignKey("workflow.id"), nullable=False)

    workflow_run_states = db.relationship(
        "WorkflowRunState", backref="workflow_run", lazy="select"
    )
    workflow_pipeline_runs = db.relationship(
        "WorkflowPipelineRun", backref="workflow_run", lazy="select"
    )


class WorkflowRunState(CommonColumnsMixin, db.Model):
    """ A lookup table of states of a WorkflowRun """

    __tablename__ = "workflowrunstate"

    workflow_run_id = db.Column(
        db.Integer, db.ForeignKey("workflowrun.id"), nullable=False
    )
    run_state_type_id = db.Column(
        db.Integer, db.ForeignKey("runstatetype.id"), nullable=False
    )


class WorkflowPipelineRun(CommonColumnsMixin, db.Model):
    """ An execution of a PipelineRun of a WorkflowRun """

    __tablename__ = "workflowpipelinerun"

    workflow_run_id = db.Column(
        db.Integer, db.ForeignKey("workflowrun.id"), nullable=False
    )
    pipeline_run_id = db.Column(
        db.Integer, db.ForeignKey("pipelinerun.id"), nullable=False
    )
    workflow_pipeline_id = db.Column(
        db.Integer, db.ForeignKey("workflowpipeline.id"), nullable=False
    )
