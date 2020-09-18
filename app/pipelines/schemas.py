from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from ..model_utils import RunStateEnum


class InputSchema(Schema):
    """ A pipeline run input. """

    name = fields.Str()
    url = fields.Url()


class CreateRunSchema(Schema):
    """ Validation schema for create_run() """

    inputs = fields.Nested(InputSchema, many=True)
    callback_url = fields.Url()


class UpdateRunStateSchema(Schema):
    """ Validation schema for update_run_status() """

    state = EnumField(RunStateEnum)
