from marshmallow import Schema, fields


class InputSchema(Schema):
    name = fields.Str()
    url = fields.Url()


class CreateRunSchema(Schema):
    inputs = fields.Nested(InputSchema, many=True)
    callback_url = fields.Url()
