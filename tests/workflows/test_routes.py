from unittest.mock import patch

import responses

from app.constants import (
    AUTH_HOSTNAME,
)
from application_roles.services import create_application
from app.utils import ApplicationsEnum
from app.constants import WORKFLOW_HOSTNAME
from app.workflows.models import (
    OrganizationWorkflow,
    db,
)
from app.workflows.queries import find_organization_workflows
from application_roles.decorators import ROLES_KEY
from requests import HTTPError

from ..conftest import (
    JWT_TOKEN,
    ORGANIZATION_UUID,
    WORKFLOW_UUID,
)
from .test_services import (
    WORKFLOW_JSON,
)


def test_requests_have_cors(app, client, client_application):
    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows",
        content_type="application/json",
    )
    assert result.headers["Access-Control-Allow-Origin"] == "*"


def test_workflows_no_roles_provided(app, client, client_application):
    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows",
        content_type="application/json",
    )
    assert result.status_code == 401

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
        },
    )
    assert result.status_code == 401


@responses.activate
def test_workflows_backing_error(app, client, client_application):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/search",
        status=500,
    )

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503


@responses.activate
def test_workflows_bad_search(app, client, client_application):
    json_response = {
        "errors": {"uuids": {"0": ["String does not match expected pattern."]}},
        "message": "Unable to search workflow",
    }
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/search",
        json=json_response,
        status=400,
    )

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert result.json == json_response


@responses.activate
def test_workflows(
    app,
    client,
    client_application,
    organization_workflow,
):
    workflow_json = dict(WORKFLOW_JSON)

    json_response = [workflow_json]
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/search",
        json=json_response,
    )

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 200
    json_response[0]["uuid"] = organization_workflow.uuid
    assert result.json == json_response


@patch("app.workflows.routes.create_workflow")
@responses.activate
def test_create_workflow_backend_500(
    create_workflow_mock, app, client, client_application
):
    create_workflow_mock.side_effect = HTTPError("something is wrong")
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows",
        content_type="application/json",
        json=WORKFLOW_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert result.json == {"message": "something is wrong"}


@patch("app.workflows.routes.create_workflow")
@responses.activate
def test_create_workflow_backend_error(
    create_workflow_mock, app, client, client_application
):
    message = {"message": "error"}
    create_workflow_mock.side_effect = ValueError(message)
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows",
        content_type="application/json",
        json=WORKFLOW_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert result.json == message


@responses.activate
def test_create_workflow(app, client, client_application):
    json_response = dict(WORKFLOW_JSON)
    json_response.update(
        {
            "created_at": "2020-10-08T12:20:36.564095",
            "updated_at": "2020-10-08T12:20:36.564100",
            "uuid": "daf6febec1714ac79a73327760c89f15",
        }
    )
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows",
        json=json_response,
    )

    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows",
        content_type="application/json",
        json=WORKFLOW_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 200

    workflow = OrganizationWorkflow.query.order_by(
        OrganizationWorkflow.id.desc()
    ).first()
    json_response["uuid"] = workflow.uuid
    assert result.json == json_response


@patch("app.workflows.routes.fetch_workflow")
@responses.activate
def test_get_workflow_backend_500(
    mock_get, app, client, client_application, organization_workflow
):
    mock_get.side_effect = HTTPError("something is wrong")
    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows/{organization_workflow.uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert result.json == {"message": "something is wrong"}


@patch("app.workflows.routes.fetch_workflow")
@responses.activate
def test_get_workflow_backend_error(
    mock_get, app, client, client_application, organization_workflow
):
    message = {"message": "error"}
    mock_get.side_effect = ValueError(message)
    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows/{organization_workflow.uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert result.json == message


@responses.activate
def test_get_workflow(app, client, client_application, organization_workflow):
    json_response = dict(WORKFLOW_JSON)

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}",
        json=json_response,
    )

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows/{organization_workflow.uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 200

    workflow = OrganizationWorkflow.query.order_by(
        OrganizationWorkflow.id.desc()
    ).first()
    json_response["uuid"] = workflow.workflow_uuid
    assert result.json == json_response


@patch("app.workflows.routes.update_workflow")
@responses.activate
def test_update_workflow_backend_500(
    mock_update, app, client, client_application, organization_workflow
):
    mock_update.side_effect = HTTPError("something is wrong")
    updates = {"name": "123", "description": "456"}
    result = client.put(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows/{organization_workflow.uuid}",
        content_type="application/json",
        json=updates,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert result.json == {"message": "something is wrong"}


@patch("app.workflows.routes.update_workflow")
@responses.activate
def test_update_workflow_backend_error(
    mock_update, app, client, client_application, organization_workflow
):
    message = {"message": "error"}
    updates = {"name": "123", "description": "456"}
    mock_update.side_effect = ValueError(message)
    result = client.put(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows/{organization_workflow.uuid}",
        content_type="application/json",
        json=updates,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert result.json == message


@responses.activate
def test_get_workflow(app, client, client_application, organization_workflow):
    json_response = dict(WORKFLOW_JSON)
    updates = {"name": "123", "description": "456"}
    json_response.update(updates)

    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}",
        json=json_response,
    )

    result = client.put(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows/{organization_workflow.uuid}",
        content_type="application/json",
        json=updates,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 200

    workflow = OrganizationWorkflow.query.order_by(
        OrganizationWorkflow.id.desc()
    ).first()
    json_response["uuid"] = workflow.workflow_uuid
    assert result.json == json_response
