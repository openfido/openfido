from application_roles.model_utils import get_db, CommonColumnsMixin

db = get_db()


class OrganizationWorkflow(CommonColumnsMixin, db.Model):
    """ Organization workflow. """

    __tablename__ = "organization_workflow"

    organization_uuid = db.Column(db.String(32), nullable=False, server_default="")
    workflow_uuid = db.Column(db.String(32), nullable=False, server_default="")
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)

    organization_workflow_pipelines = db.relationship(
        "OrganizationWorkflowPipeline",
        backref=db.backref("organization_workflow_pipeline"),
        lazy="immediate",
        primaryjoin="foreign(OrganizationWorkflow.id) == remote(OrganizationWorkflowPipeline.id)",
    )


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
        backref=db.backref("organization_workflow_pipeline"),
        lazy="immediate",
        primaryjoin="remote(OrganizationWorkflow.id) == foreign(OrganizationWorkflowPipeline.id)",
    )

    organization_workflow_pipeline_runs = db.relationship(
        "OrganizationWorkflowPipelineRun",
        backref="organization_workflow_pipeline_run",
        lazy="immediate",
        primaryjoin="remote(OrganizationWorkflowPipelineRun.id) == foreign(OrganizationWorkflowPipeline.id)",
    )


class OrganizationWorkflowPipelineRun(CommonColumnsMixin, db.Model):
    """ Organization workflow run """

    __tablename__ = "organization_workflow_pipeline_run"

    organization_workflow_id = db.Column(
        db.Integer, db.ForeignKey("organization_workflow.id"), nullable=False
    )
    organization_pipeline_run_id = db.Column(
        db.Integer, db.ForeignKey("organization_pipeline_run.id"), nullable=False
    )

    organization_workflow_run_id = db.Column(
        db.Integer, db.ForeignKey("organization_workflow_run.id"), nullable=False
    )
    workflow_run_uuid = db.Column(db.String(32), nullable=True, server_default="")
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)


class OrganizationWorkflowRun(CommonColumnsMixin, db.Model):
    """ Organization workflow run """

    __tablename__ = "organization_workflow_run"

    organization_workflow_uuid = db.Column(
        db.String(32), nullable=False, server_default=""
    )
    workflow_run_uuid = db.Column(db.String(32), nullable=False, server_default="")
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)
