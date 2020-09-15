from marshmallow import Schema, fields, validate

from .models import Workflow


class WorkflowSchema(Schema):
    """ Serialized public view of a Workflow. """

    uuid = fields.Str()
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
