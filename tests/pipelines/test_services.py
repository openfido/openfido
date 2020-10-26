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
def test_fetch_pipelines_bad_workflow_response(post_mock, app, organization_pipeline):
    pipeline_list = [
        {
            "uuid": "nonexistant-organization-organization_pipeline-uuid",
            "name": "name 1",
        }
    ]
    post_mock().json.return_value = pipeline_list

    expected_result = [{"uuid": organization_pipeline.uuid, "name": "name 1"}]

    # we got back bogus workflow service data, but we did make the API call:
    with pytest.raises(HTTPError):
        fetch_pipelines(ORGANIZATION_UUID)

    post_mock.assert_called()
    get_call = post_mock.call_args
    assert get_call[0][0].startswith(app.config[WORKFLOW_HOSTNAME])
    assert get_call[1]["headers"][ROLES_KEY] == app.config[WORKFLOW_API_TOKEN]
    assert get_call[1]["json"] == {"uuids": [organization_pipeline.pipeline_uuid]}

    post_mock().raise_for_status.assert_called()
    post_mock().json.assert_called()


@patch("app.pipelines.services.requests.post")
def test_fetch_pipelines(post_mock, app, organization_pipeline):
    pipeline_list = [{"uuid": organization_pipeline.pipeline_uuid, "name": "name 1"}]
    post_mock().json.return_value = pipeline_list

    expected_result = [{"uuid": organization_pipeline.uuid, "name": "name 1"}]
    assert fetch_pipelines(ORGANIZATION_UUID) == expected_result
    post_mock.assert_called()
    get_call = post_mock.call_args
    assert get_call[0][0].startswith(app.config[WORKFLOW_HOSTNAME])
    assert get_call[1]["headers"][ROLES_KEY] == app.config[WORKFLOW_API_TOKEN]
    assert get_call[1]["json"] == {"uuids": [organization_pipeline.pipeline_uuid]}

    post_mock().raise_for_status.assert_called()
    post_mock().json.assert_called()


@responses.activate
def test_update_pipeline_bad_response(app, organization_pipeline):
    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
        json=PIPELINE_JSON,
        status=500,
    )
    with pytest.raises(ValueError):
        update_pipeline(ORGANIZATION_UUID, organization_pipeline.uuid, PIPELINE_JSON)


def test_update_pipeline_no_pipeline(app):
    with pytest.raises(ValueError):
        update_pipeline(ORGANIZATION_UUID, PIPELINE_UUID, PIPELINE_JSON)


@responses.activate
def test_update_pipeline_bad_json(app, organization_pipeline):
    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
        body="notjson",
    )
    with pytest.raises(HTTPError):
        update_pipeline(ORGANIZATION_UUID, organization_pipeline.uuid, PIPELINE_JSON)


@responses.activate
def test_update_pipeline(app, organization_pipeline):
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
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
        json=json_response,
    )
    updated_pipeline = update_pipeline(
        ORGANIZATION_UUID, organization_pipeline.uuid, PIPELINE_JSON
    )
    organization_pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()
    json_response["uuid"] = organization_pipeline.uuid
    assert updated_pipeline == json_response


@responses.activate
def test_delete_pipeline_no_pipeline(app, organization_pipeline):
    with pytest.raises(ValueError):
        delete_pipeline(ORGANIZATION_UUID, "badid")
    organization_pipeline = set(OrganizationPipeline.query.all()) == set(
        [organization_pipeline]
    )


@responses.activate
def test_delete_pipeline(app, organization_pipeline):
    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
    )
    delete_pipeline(ORGANIZATION_UUID, organization_pipeline.uuid)

    assert organization_pipeline.is_deleted
