from marshmallow import Schema, fields, validate


def UUID(*args, **kwargs):
    """
    A uuid validating field (marshmallow's UUID field modifies the string, this
    version does not).
    """
    kwargs["validate"] = validate.Regexp(r"[a-f0-9]{32}")
    return fields.String(*args, **kwargs)


class PipelineDependencySchema(Schema):
    """ A pipeline UUID and any dependencies. """
    uuid = UUID(required=True)
    dependencies = fields.List(UUID(), missing=[])


class CreateWorkflowSchema(Schema):
    """ JSON format for creating workflows """

    name = fields.Str(required=True)
    description = fields.Str(required=True)
    pipelines = fields.Nested(PipelineDependencySchema, many=True, required=True)
