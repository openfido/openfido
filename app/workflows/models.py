from application_roles.model_utils import get_db, CommonColumnsMixin

db = get_db()


class OrganizationWorkflow(CommonColumnsMixin, db.Model):
    """ Organization workflow. """

    __tablename__ = "organization_workflow"

    organization_uuid = db.Column(db.String(32), nullable=False, server_default="")
    workflow_uuid = db.Column(db.String(32), nullable=False, server_default="")
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)


class OrganizationWorkflowPipeline(CommonColumnsMixin, db.Model):
    """ Organization workflow pipeline. """

    __tablename__ = "organization_workflow_pipeline"

    organization_workflow_uuid = db.Column(
        db.String(32), nullable=False, server_default=""
    )
    organization_pipeline_id = db.Column(
        db.Integer, db.ForeignKey("organization_pipeline.id"), nullable=False
    )
    workflow_pipeline_uuid = db.Column(db.String(32), nullable=False, server_default="")
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)

    organization_workflow = db.relationship(
        OrganizationWorkflow,
        backref=db.backref("organization_workflow_pipelines"),
        primaryjoin="remote(OrganizationWorkflow.uuid) == foreign(OrganizationWorkflowPipeline.organization_workflow_uuid)",
    )


class OrganizationWorkflowPipelineRun(CommonColumnsMixin, db.Model):
    """ Organization workflow pipeline run """

    __tablename__ = "organization_workflow_pipeline_run"

    organization_workflow_id = db.Column(
        db.Integer, db.ForeignKey("organization_workflow.id"), nullable=False
    )
    organization_pipeline_run_id = db.Column(
        db.Integer, db.ForeignKey("organization_pipeline_run.id"), nullable=False
    )
    workflow_run_uuid = db.Column(db.String(32), nullable=False, server_default="")
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)
