from application_roles.model_utils import CommonColumnsMixin, get_db

db = get_db()


class OrganizationPipeline(CommonColumnsMixin, db.Model):
    """ Represents a 'pipeline' job of a specific organization. """

    __tablename__ = "organization_pipeline"

    organization_uuid = db.Column(db.String(32), nullable=False, server_default="")
    pipeline_uuid = db.Column(db.String(32), nullable=False, server_default="")
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)

    organization_pipeline_runs = db.relationship(
        "OrganizationPipelineRun", backref="organization_pipeline", lazy="immediate"
    )

    organization_pipeline_input_files = db.relationship(
        "OrganizationPipelineInputFile",
        backref="organization_pipeline",
        lazy="immediate",
    )

    organization_workflow_pipelines = db.relationship(
        "OrganizationWorkflowPipeline",
        backref="organization_pipeline",
        lazy="select",
    )


class OrganizationPipelineInputFile(CommonColumnsMixin, db.Model):
    """ An input file associated with a OrganizationPipeline. """

    __tablename__ = "organization_pipeline_input_file"

    name = db.Column(db.String(200), nullable=False, server_default="")

    organization_pipeline_run_id = db.Column(
        db.Integer, db.ForeignKey("organization_pipeline_run.id"), nullable=True
    )

    organization_pipeline_id = db.Column(
        db.Integer, db.ForeignKey("organization_pipeline.id"), nullable=False
    )


class OrganizationPipelineRun(CommonColumnsMixin, db.Model):
    """ A pipeline run within an organization """

    __tablename__ = "organization_pipeline_run"

    organization_pipeline_id = db.Column(
        db.Integer, db.ForeignKey("organization_pipeline.id"), nullable=False
    )

    pipeline_run_uuid = db.Column(db.String(32), nullable=True)

    post_processing_pipeline_run_uuid = db.Column(
        db.String(32), nullable=False, server_default=""
    )

    status_update_token = db.Column(db.String(32), nullable=False)
    status_update_token_expires_at = db.Column(db.DateTime, nullable=False)

    share_token = db.Column(db.String(32), nullable=False)
    share_password_hash = db.Column(db.String(127), nullable=True)
    share_password_salt = db.Column(db.String(127), nullable=True)

    organization_pipeline_run_post_processing_states = db.relationship(
        "OrganizationPipelineRunPostProcessingState",
        backref="organization_pipeline_run",
        lazy="immediate",
    )

    artifact_charts = db.relationship(
        "ArtifactChart",
        backref="organization_pipeline_run",
        lazy="select",
    )


class ArtifactChart(CommonColumnsMixin, db.Model):
    """ A pipeline run within an organization """

    __tablename__ = "artifact_chart"

    name = db.Column(db.String(128), nullable=False)
    is_deleted = db.Column(db.Boolean(), default=False, nullable=True)
    organization_pipeline_run_id = db.Column(
        db.Integer, db.ForeignKey("organization_pipeline_run.id"), nullable=False
    )

    artifact_uuid = db.Column(db.String(32), nullable=False)
    chart_type_code = db.Column(db.String(20), nullable=False)
    chart_config = db.Column(db.JSON(), nullable=False)


class PostProcessingState(CommonColumnsMixin, db.Model):
    """ Lookup table status codes of post processing jobs """

    __tablename__ = "post_processing_state"

    name = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(20), nullable=False)

    organization_pipeline_run_post_processing_states = db.relationship(
        "OrganizationPipelineRunPostProcessingState",
        backref="post_processing_state",
        lazy="select",
    )


class OrganizationPipelineRunPostProcessingState(CommonColumnsMixin, db.Model):
    """ The statuses of on organization pipeline """

    __tablename__ = "organization_pipeline_run_post_processing_state"

    organization_pipeline_run_id = db.Column(
        db.Integer, db.ForeignKey("organization_pipeline_run.id"), nullable=False
    )

    post_processing_state_id = db.Column(
        db.Integer, db.ForeignKey("post_processing_state.id"), nullable=False
    )
