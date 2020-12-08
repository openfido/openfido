from marshmallow import Schema, fields, validate

from .models import ArtifactChart


# TODO refactor into openfido-utils (this is also used in openfido-workflow-service)
def UUID(*args, **kwargs):
    """
    A uuid validating field (marshmallow's UUID field modifies the string, this
    version does not).
    """
    kwargs["validate"] = validate.Regexp(r"[a-f0-9]{32}")
    return fields.String(*args, **kwargs)


class CreateArtifactChart(Schema):
    """ Validation schema for create_artifact_chart() """

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=ArtifactChart.name.type.length),
    )
    artifact_uuid = UUID(required=True)
    chart_type_code = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=ArtifactChart.chart_type_code.type.length),
    )
    chart_config = fields.Field(missing={})
