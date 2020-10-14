from unittest.mock import patch

import pytest
import responses
from app.constants import WORKFLOW_API_TOKEN, WORKFLOW_HOSTNAME
from app.pipelines.models import OrganizationPipeline
from app.pipelines.services import (
    create_pipeline,
    fetch_pipelines,
    update_pipeline,
    delete_pipeline,
)
from application_roles.decorators import ROLES_KEY
from requests import HTTPError

from ..conftest import ORGANIZATION_UUID, PIPELINE_UUID

PIPELINE_JSON = {
    "description": "a pipeline",
    "docker_image_url": "python:3",
    "name": "pipeline 1",
    "repository_branch": "master",
    "repository_ssh_url": "https://github.com/PresencePG/presence-pipeline-example.git",
}


@responses.activate
def test_create_pipeline_bad_response(app):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines",
        json=PIPELINE_JSON,
        status=500,
    )
    with pytest.raises(ValueError):
        create_pipeline(ORGANIZATION_UUID, PIPELINE_JSON)


@responses.activate
def test_create_pipeline_bad_json(app):
    responses.add(
        responses.POST, f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines", body="notjson"
    )
    with pytest.raises(HTTPError):
        create_pipeline(ORGANIZATION_UUID, PIPELINE_JSON)


@responses.activate
def test_create_pipeline(app):
    json_response = dict(PIPELINE_JSON)
    json_response.update(
        {
            "created_at": "2020-10-08T14:22:26.276242",
            "updated_at": "2020-10-08T14:22:26.276278",
            "uuid": "83ac3b4e9433431fbd6d21e7a56b6f0a",
        }
    )
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines",
        json=json_response,
    )
    created_pipeline = create_pipeline(ORGANIZATION_UUID, PIPELINE_JSON)
    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()
    json_response["uuid"] = pipeline.uuid
    assert created_pipeline == json_response


@patch("app.pipelines.services.requests.post")
def test_fetch_pipelines(post_mock, app):
    post_mock().json.return_value = ["somedata"]

    assert fetch_pipelines(ORGANIZATION_UUID) == ["somedata"]
    post_mock.assert_called()
    get_call = post_mock.call_args
    assert get_call[0][0].startswith(app.config[WORKFLOW_HOSTNAME])
    assert get_call[1]["headers"][ROLES_KEY] == app.config[WORKFLOW_API_TOKEN]
    assert get_call[1]["json"] == {"uuids": []}

    post_mock().raise_for_status.assert_called()
    post_mock().json.assert_called()


@responses.activate
def test_update_pipeline_bad_response(app, pipeline):
    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{pipeline.pipeline_uuid}",
        json=PIPELINE_JSON,
        status=500,
    )
    with pytest.raises(ValueError):
        update_pipeline(ORGANIZATION_UUID, pipeline.uuid, PIPELINE_JSON)


def test_update_pipeline_no_pipeline(app):
    with pytest.raises(ValueError):
        update_pipeline(ORGANIZATION_UUID, PIPELINE_UUID, PIPELINE_JSON)


@responses.activate
def test_update_pipeline_bad_json(app, pipeline):
    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{pipeline.pipeline_uuid}",
        body="notjson",
    )
    with pytest.raises(HTTPError):
        update_pipeline(ORGANIZATION_UUID, pipeline.uuid, PIPELINE_JSON)


@responses.activate
def test_update_pipeline(app, pipeline):
    json_response = dict(PIPELINE_JSON)
    json_response.update(
        {
            "updated_at": "2020-10-08T14:22:26.276242",
            "updated_at": "2020-10-08T14:22:26.276278",
            "uuid": "83ac3b4e9433431fbd6d21e7a56b6f0a",
        }
    )
    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{pipeline.pipeline_uuid}",
        json=json_response,
    )
    updated_pipeline = update_pipeline(ORGANIZATION_UUID, pipeline.uuid, PIPELINE_JSON)
    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()
    json_response["uuid"] = pipeline.uuid
    assert updated_pipeline == json_response


@responses.activate
def test_delete_pipeline_no_pipeline(app, pipeline):
    with pytest.raises(ValueError):
        delete_pipeline(ORGANIZATION_UUID, "badid")
    pipeline = set(OrganizationPipeline.query.all()) == set([pipeline])


@responses.activate
def test_delete_pipeline(app, pipeline):
    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{pipeline.pipeline_uuid}",
    )
    delete_pipeline(ORGANIZATION_UUID, pipeline.uuid)

    assert pipeline.is_deleted
