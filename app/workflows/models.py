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


class WorkflowPipeline(CommonColumnsMixin, db.Model):
    """ A pipeline that is part of a workflow. """

    __tablename__ = "workflow_pipeline"

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


class WorkflowPipelineDependency(CommonColumnsMixin, db.Model):
    """ A dependency between pipelines. """

    __tablename__ = "workflow_pipeline_dependency"

    from_workflow_pipeline_id = db.Column(
        db.Integer, db.ForeignKey("workflow_pipeline.id"), nullable=False
    )

    to_workflow_pipeline_id = db.Column(
        db.Integer, db.ForeignKey("workflow_pipeline.id"), nullable=False
    )
