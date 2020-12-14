from blob_utils.schemas import UUID
from marshmallow import Schema, fields, validate


class PipelineDependencySchema(Schema):
    """ A pipeline UUID and any dependencies. """
    uuid = UUID(required=True)
    dependencies = fields.List(UUID(), missing=[])


class CreateWorkflowSchema(Schema):
    """ JSON format for creating workflows """

    name = fields.Str(required=True)
    description = fields.Str(required=True)
    pipelines = fields.Nested(PipelineDependencySchema, many=True, required=True)
