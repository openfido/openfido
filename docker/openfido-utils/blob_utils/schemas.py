from marshmallow import fields, validate


def UUID(*args, **kwargs):
    """
    A uuid validating field (marshmallow's UUID field modifies the string, this
    version does not).
    """
    kwargs["validate"] = validate.Regexp(r"[a-f0-9]{32}")
    return fields.String(*args, **kwargs)
