from marshmallow import Schema, fields, validate

from .models import Workflow
from ..schemas import UUID


class WorkflowSchema(Schema):
    """ Serialized public view of a Workflow. """

    uuid = UUID()
    name = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class CreateWorkflowSchema(Schema):
    """ Schema for create_workflow() service. """

    name = fields.Str(
        required=True, validate=validate.Length(min=1, max=Workflow.name.type.length)
    )
    description = fields.Str(
        required=True, validate=validate.Length(max=Workflow.description.type.length)
    )


class CreateWorkflowPipelineSchema(Schema):
    """ Schema for create_workflow_pipeline() service. """

    pipeline_uuid = UUID()
    source_workflow_pipelines = fields.List(UUID())
    destination_workflow_pipelines = fields.List(UUID())
