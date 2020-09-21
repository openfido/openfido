from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from ..model_utils import RunStateEnum
from ..schemas import UUID


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


class PipelineSchema(Schema):
    """ Serialized public view of a Workflow. """

    uuid = fields.Str()
    name = fields.Str()
    description = fields.Str()
    docker_image_url = fields.Str()
    repository_ssh_url = fields.Str()
    repository_branch = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class SearchPipelinesSchema(Schema):
    """ Schema for find_pipelines() queries. """

    uuids = fields.List(UUID())
