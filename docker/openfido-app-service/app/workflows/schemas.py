from marshmallow import Schema, fields
from blob_utils.schemas import UUID


class CreateWorkflowPipelineSchema(Schema):
    """ Schema for create_workflow_pipeline() service. """

    pipeline_uuid = UUID(required=True)
    source_workflow_pipelines = fields.List(UUID(), required=True)
    destination_workflow_pipelines = fields.List(UUID(), required=True)
