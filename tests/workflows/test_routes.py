import copy

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
    OrganizationWorkflowPipeline,
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
    WORKFLOW_PIPELINE_RESPONSE_JSON,
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

    json_response["uuid"] = organization_workflow.uuid

    assert result.status_code == 200
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
def test_update_workflow(app, client, client_application, organization_workflow):
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

    json_response["uuid"] = organization_workflow.uuid

    assert result.status_code == 200
    assert result.json == json_response


@responses.activate
def test_delete_workflow_invalid_org_workflow(
    app, client, client_application, organization_workflow
):
    result = client.delete(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows/1234",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 400


@responses.activate
def test_delete_workflow_invalid_workflow(
    app, client, client_application, organization_workflow
):
    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}",
        json={"not": "found"},
        status=404,
    )

    result = client.delete(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows/{organization_workflow.uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 503


@responses.activate
def test_delete_workflow(app, client, client_application, organization_workflow):
    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}",
        json={},
    )

    result = client.delete(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows/{organization_workflow.uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 200
    assert result.json == {}


@patch("app.workflows.routes.create_workflow_pipeline")
@responses.activate
def test_workflow_pipeline_create_backend_500(
    create_mock, app, client, client_application, organization_workflow
):
    create_mock.side_effect = HTTPError("something is wrong")
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows/{organization_workflow.uuid}/pipelines",
        content_type="application/json",
        json=WORKFLOW_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert result.json == {"message": "something is wrong"}


@patch("app.workflows.routes.create_workflow_pipeline")
@responses.activate
def test_workflow_pipeline_create_backend_error(
    create_mock, app, client, client_application, organization_workflow
):
    message = {"message": "error"}
    create_mock.side_effect = ValueError(message)
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows/{organization_workflow.uuid}/pipelines",
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
def test_workflow_pipeline_create(
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}/pipelines",
        json=WORKFLOW_PIPELINE_RESPONSE_JSON,
    )

    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/workflows/{organization_workflow.uuid}/pipelines",
        content_type="application/json",
        json={
            "pipeline_uuid": organization_pipeline.uuid,
            "source_workflow_pipelines": [
                organization_workflow_pipeline.uuid,
            ],
            "destination_workflow_pipelines": [
                organization_workflow_pipeline.uuid,
            ],
        },
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    new_org_workflow_pipeline = result.json
    created_org_workflow_pipeline = OrganizationWorkflowPipeline.query.filter(
        OrganizationWorkflowPipeline.uuid == new_org_workflow_pipeline.get("uuid")
    ).first()

    assert result.status_code == 200
    assert new_org_workflow_pipeline["uuid"] == created_org_workflow_pipeline.uuid


@patch("app.workflows.routes.fetch_workflow_pipelines")
@responses.activate
def test_workflow_pipelines_backend_500(
    fetch_mock,
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):
    fetch_mock.side_effect = HTTPError("something is wrong")
    result = client.get(
        f"/v1/organizations/{organization_workflow.organization_uuid}/workflows/{organization_workflow.uuid}/pipelines",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert result.json == {"message": "something is wrong"}


@patch("app.workflows.routes.fetch_workflow_pipelines")
@responses.activate
def test_workflow_pipelines_backend_error(
    fetch_mock,
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):
    message = {"message": "error"}
    fetch_mock.side_effect = ValueError(message)
    result = client.get(
        f"/v1/organizations/{organization_workflow.organization_uuid}/workflows/{organization_workflow.uuid}/pipelines",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert result.json == message


@responses.activate
def test_workflow_pipelines(
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}/pipelines",
        json=[WORKFLOW_PIPELINE_RESPONSE_JSON],
    )

    result = client.get(
        f"/v1/organizations/{organization_workflow.organization_uuid}/workflows/{organization_workflow.uuid}/pipelines",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    # verify pipeline and src/dest (which should reference itself)
    first_result = result.json[0]
    assert first_result["pipeline_uuid"] == organization_pipeline.uuid
    assert (
        str(organization_workflow_pipeline.uuid)
        in first_result["destination_workflow_pipelines"]
    )
    assert (
        str(organization_workflow_pipeline.uuid)
        in first_result["source_workflow_pipelines"]
    )


@patch("app.workflows.routes.fetch_workflow_pipeline")
@responses.activate
def test_workflow_pipeline_backend_500(
    fetch_mock,
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):
    fetch_mock.side_effect = HTTPError("something is wrong")

    org_uuid = organization_workflow.organization_uuid
    ow_wf_uuid = organization_workflow.uuid
    ow_wf_pipeline_uuid = organization_workflow_pipeline.uuid

    result = client.get(
        f"/v1/organizations/{org_uuid}/workflows/{ow_wf_uuid}/pipelines/{ow_wf_pipeline_uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert result.json == {"message": "something is wrong"}


@patch("app.workflows.routes.fetch_workflow_pipeline")
@responses.activate
def test_workflow_pipeline_backend_error(
    fetch_mock,
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):
    message = {"message": "error"}
    fetch_mock.side_effect = ValueError(message)

    org_uuid = organization_workflow.organization_uuid
    ow_wf_uuid = organization_workflow.uuid
    ow_wf_pipeline_uuid = organization_workflow_pipeline.uuid

    result = client.get(
        f"/v1/organizations/{org_uuid}/workflows/{ow_wf_uuid}/pipelines/{ow_wf_pipeline_uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 400
    assert result.json == message


@responses.activate
def test_workflow_pipelines(
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):
    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/pipelines/{wf_pipeline_uuid}",
        json=WORKFLOW_PIPELINE_RESPONSE_JSON,
    )

    org_uuid = organization_workflow.organization_uuid
    ow_wf_uuid = organization_workflow.uuid
    ow_wf_pipeline_uuid = organization_workflow_pipeline.uuid

    result = client.get(
        f"/v1/organizations/{org_uuid}/workflows/{ow_wf_uuid}/pipelines/{ow_wf_pipeline_uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    ow_pipeline = result.json
    assert ow_pipeline["pipeline_uuid"] == organization_pipeline.uuid

    for key in ["destination_workflow_pipelines", "source_workflow_pipelines"]:
        str(organization_workflow_pipeline.uuid) in ow_pipeline[key]


@patch("app.workflows.routes.update_workflow_pipeline")
@responses.activate
def test_workflow_pipeline_update_backend_500(
    update_mock,
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):
    update_mock.side_effect = HTTPError("something is wrong")

    org_uuid = organization_workflow.organization_uuid
    ow_wf_uuid = organization_workflow.uuid
    ow_wf_pipeline_uuid = organization_workflow_pipeline.uuid

    result = client.put(
        f"/v1/organizations/{org_uuid}/workflows/{ow_wf_uuid}/pipelines/{ow_wf_pipeline_uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
        json={
            "pipeline_uuid": organization_workflow_pipeline.uuid,
        },
    )
    assert result.status_code == 503
    assert result.json == {"message": "something is wrong"}


@patch("app.workflows.routes.update_workflow_pipeline")
@responses.activate
def test_workflow_pipeline_update_backend_error(
    update_mock,
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):
    message = {"message": "error"}
    update_mock.side_effect = ValueError(message)

    org_uuid = organization_workflow.organization_uuid
    ow_wf_uuid = organization_workflow.uuid
    ow_wf_pipeline_uuid = organization_workflow_pipeline.uuid

    result = client.put(
        f"/v1/organizations/{org_uuid}/workflows/{ow_wf_uuid}/pipelines/{ow_wf_pipeline_uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
        json={
            "pipeline_uuid": organization_workflow_pipeline.uuid,
        },
    )

    assert result.status_code == 400
    assert result.json == message


@responses.activate
def test_workflow_pipeline_update(
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):
    # add additional workflow pipelines to this workflow pipeline
    mock_updated = copy.deepcopy(WORKFLOW_PIPELINE_RESPONSE_JSON)
    mock_updated["source_workflow_pipelines"].append(
        organization_workflow_pipeline.uuid
    )
    mock_updated["destination_workflow_pipelines"].append(
        organization_workflow_pipeline.uuid
    )

    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/pipelines/{wf_pipeline_uuid}",
        json=mock_updated,
    )

    org_uuid = organization_workflow.organization_uuid
    ow_wf_uuid = organization_workflow.uuid
    ow_wf_pipeline_uuid = organization_workflow_pipeline.uuid

    update_result = client.put(
        f"/v1/organizations/{org_uuid}/workflows/{ow_wf_uuid}/pipelines/{ow_wf_pipeline_uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
        json={
            "source_workflow_pipelines": [
                organization_workflow_pipeline.uuid,
                organization_workflow_pipeline.uuid,
            ],
            "pipeline_uuid": organization_pipeline.uuid,
            "destination_workflow_pipelines": [
                organization_workflow_pipeline.uuid,
                organization_workflow_pipeline.uuid,
            ],
        },
    )

    ow_pipeline = update_result.json

    assert ow_pipeline["pipeline_uuid"] == organization_pipeline.uuid

    for key in ["source_workflow_pipelines", "destination_workflow_pipelines"]:
        assert all(
            ow_p == organization_workflow_pipeline.uuid for ow_p in ow_pipeline[key]
        )


@patch("app.workflows.routes.delete_workflow_pipeline")
@responses.activate
def test_workflow_pipeline_delete_backend_500(
    delete_mock,
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):
    delete_mock.side_effect = HTTPError("something is wrong")

    org_uuid = organization_workflow.organization_uuid
    ow_wf_uuid = organization_workflow.uuid
    ow_wf_pipeline_uuid = organization_workflow_pipeline.uuid

    result = client.delete(
        f"/v1/organizations/{org_uuid}/workflows/{ow_wf_uuid}/pipelines/{ow_wf_pipeline_uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert result.json == {"message": "something is wrong"}


@patch("app.workflows.routes.delete_workflow_pipeline")
@responses.activate
def test_workflow_pipeline_delete_backend_error(
    delete_mock,
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):
    message = {"message": "error"}
    delete_mock.side_effect = ValueError(message)

    org_uuid = organization_workflow.organization_uuid
    ow_wf_uuid = organization_workflow.uuid
    ow_wf_pipeline_uuid = organization_workflow_pipeline.uuid

    result = client.delete(
        f"/v1/organizations/{org_uuid}/workflows/{ow_wf_uuid}/pipelines/{ow_wf_pipeline_uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 400
    assert result.json == message


@responses.activate
def test_workflow_pipeline_delete(
    app,
    client,
    client_application,
    organization_workflow,
    organization_pipeline,
    organization_workflow_pipeline,
):

    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/pipelines/{wf_pipeline_uuid}",
        status=204,
    )

    org_uuid = organization_workflow.organization_uuid
    ow_wf_uuid = organization_workflow.uuid
    ow_wf_pipeline_uuid = organization_workflow_pipeline.uuid

    result = client.delete(
        f"/v1/organizations/{org_uuid}/workflows/{ow_wf_uuid}/pipelines/{ow_wf_pipeline_uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    ow_pipeline = OrganizationWorkflowPipeline.query.filter(
        OrganizationWorkflowPipeline.uuid == organization_workflow_pipeline.uuid
    ).first()

    assert ow_pipeline.is_deleted is True
