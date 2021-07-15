from blob_utils.schemas import UUID
from marshmallow import Schema, fields, validate

from .models import ArtifactChart


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
