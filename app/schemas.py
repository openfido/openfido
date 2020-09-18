from marshmallow import fields, validate


def UUID():
    """
    A uuid validating field (marshmallow's UUID field modifies the string, this
    version does not).
    """
    return fields.String(validate=validate.Regexp(r"[a-f0-9]{32}"))
