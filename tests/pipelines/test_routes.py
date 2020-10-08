from unittest.mock import patch

import responses
from app import db
from app.constants import WORKFLOW_HOSTNAME
from application_roles.decorators import ROLES_KEY

from ..conftest import JWT_TOKEN, ORGANIZATION_UUID, USER_UUID


@responses.activate
def test_pipelines_backing_error(app, client, client_application):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/search",
        status=500,
    )

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503


@responses.activate
def test_pipelines_bad_search(app, client, client_application):
    json_response = {
        "errors": {"uuids": {"0": ["String does not match expected pattern."]}},
        "message": "Unable to search pipeline",
    }
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/search",
        json=json_response,
        status=400,
    )

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert result.json == json_response


@responses.activate
def test_pipelines(app, client, client_application):
    json_response = [
        {
            "created_at": "2020-10-08T12:20:36.564095",
            "description": "a pipeline",
            "docker_image_url": "python:3",
            "name": "pipeline 1",
            "repository_branch": "master",
            "repository_ssh_url": "https://github.com/PresencePG/presence-pipeline-example.git",
            "updated_at": "2020-10-08T12:20:36.564100",
            "uuid": "daf6febec1714ac79a73327760c89f15",
        }
    ]
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/search",
        json=json_response,
    )

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 200
    assert result.json == json_response
