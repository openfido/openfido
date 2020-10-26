from unittest.mock import patch

import responses
from app.constants import WORKFLOW_HOSTNAME
from app.pipelines.models import OrganizationPipeline, db
from application_roles.decorators import ROLES_KEY
from requests import HTTPError
from app.pipelines.queries import find_organization_pipelines

from ..conftest import JWT_TOKEN, ORGANIZATION_UUID, USER_UUID
from .test_services import PIPELINE_JSON


def test_requests_have_cors(app, client, client_application):
    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
    )
    assert result.headers["Access-Control-Allow-Origin"] == "*"


def test_pipelines_no_roles_provided(app, client, client_application):
    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
    )
    assert result.status_code == 401

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
        },
    )
    assert result.status_code == 401


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
def test_pipelines(app, client, client_application, organization_pipeline):
    pipeline_json = dict(PIPELINE_JSON)
    pipeline_json.update(
        {
            "created_at": "2020-10-08T12:20:36.564095",
            "updated_at": "2020-10-08T12:20:36.564100",
            "uuid": organization_pipeline.pipeline_uuid,
        }
    )
    json_response = [pipeline_json]
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
    json_response[0]["uuid"] = organization_pipeline.uuid
    assert result.json == json_response


@patch("app.pipelines.routes.create_pipeline")
@responses.activate
def test_create_pipeline_backend_500(
    create_pipeline_mock, app, client, client_application
):
    create_pipeline_mock.side_effect = HTTPError("something is wrong")
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        json=PIPELINE_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert result.json == {"message": "something is wrong"}


@patch("app.pipelines.routes.create_pipeline")
@responses.activate
def test_create_pipeline_backend_error(
    create_pipeline_mock, app, client, client_application
):
    message = {"message": "error"}
    create_pipeline_mock.side_effect = ValueError(message)
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        json=PIPELINE_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert result.json == message


@responses.activate
def test_create_pipeline(app, client, client_application):
    json_response = dict(PIPELINE_JSON)
    json_response.update(
        {
            "created_at": "2020-10-08T12:20:36.564095",
            "updated_at": "2020-10-08T12:20:36.564100",
            "uuid": "daf6febec1714ac79a73327760c89f15",
        }
    )
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines",
        json=json_response,
    )

    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        json=PIPELINE_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 200

    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()
    json_response["uuid"] = pipeline.uuid
    assert result.json == json_response


@patch("app.pipelines.routes.update_pipeline")
@responses.activate
def test_update_pipeline_backend_500(
    update_pipeline_mock, app, client, client_application
):
    update_pipeline_mock.side_effect = HTTPError("something is wrong")
    result = client.put(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/" + "0" * 32,
        content_type="application/json",
        json=PIPELINE_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert result.json == {"message": "something is wrong"}


@patch("app.pipelines.routes.update_pipeline")
@responses.activate
def test_update_pipeline_backend_error(
    update_pipeline_mock, app, client, client_application
):
    message = {"message": "error"}
    update_pipeline_mock.side_effect = ValueError(message)
    result = client.put(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/" + "0" * 32,
        content_type="application/json",
        json=PIPELINE_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert result.json == message


@responses.activate
def test_update_pipeline(app, client, client_application, organization_pipeline):
    json_response = dict(PIPELINE_JSON)
    json_response.update(
        {
            "updated_at": "2020-10-08T12:20:36.564095",
            "updated_at": "2020-10-08T12:20:36.564100",
            "uuid": "daf6febec1714ac79a73327760c89f15",
        }
    )
    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
        json=json_response,
    )

    result = client.put(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}",
        content_type="application/json",
        json=PIPELINE_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 200

    organization_pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()
    json_response["uuid"] = organization_pipeline.uuid
    assert result.json == json_response


@responses.activate
def test_delete_pipeline(app, client, client_application, organization_pipeline):
    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
    )

    result = client.delete(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 200
    assert set(find_organization_pipelines(ORGANIZATION_UUID)) == set()


@patch("app.pipelines.routes.delete_pipeline")
@responses.activate
def test_delete_pipeline_http_error(
    delete_mock, app, client, client_application, organization_pipeline
):
    delete_mock.side_effect = HTTPError("something is wrong")
    result = client.delete(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert set(find_organization_pipelines(ORGANIZATION_UUID)) == set(
        [organization_pipeline]
    )
    assert result.json == {"message": "something is wrong"}


@patch("app.pipelines.routes.delete_pipeline")
@responses.activate
def test_delete_pipeline_bad_response(
    delete_mock, app, client, client_application, organization_pipeline
):
    message = {"message": "error"}
    delete_mock.side_effect = ValueError(message)
    result = client.delete(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert set(find_organization_pipelines(ORGANIZATION_UUID)) == set(
        [organization_pipeline]
    )


@responses.activate
def test_delete_pipeline(app, client, client_application, organization_pipeline):
    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
    )

    result = client.delete(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 200
    assert set(find_organization_pipelines(ORGANIZATION_UUID)) == set()
