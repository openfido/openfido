from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from .models import RunStateEnum


class InputSchema(Schema):
    name = fields.Str()
    url = fields.Url()


class CreateRunSchema(Schema):
    inputs = fields.Nested(InputSchema, many=True)
    callback_url = fields.Url()


class UpdateRunStateSchema(Schema):
    state = EnumField(RunStateEnum)
