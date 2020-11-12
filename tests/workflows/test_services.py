from unittest.mock import patch

import pytest
import responses
from app.constants import WORKFLOW_API_TOKEN, WORKFLOW_HOSTNAME
from app.workflows.models import (
    OrganizationWorkflow,
)
from app.workflows.services import (
    create_workflow,
    fetch_workflow,
    fetch_workflows,
)
from application_roles.decorators import ROLES_KEY
from requests import HTTPError

from ..conftest import (
    ORGANIZATION_UUID,
    WORKFLOW_UUID,
)

WORKFLOW_JSON = {
    "created_at": "2020-11-11T03:19:32.401965",
    "description": "A workflow that does cool things2",
    "name": "My Workflow",
    "updated_at": "2020-11-11T03:19:32.401973",
    "uuid": WORKFLOW_UUID,
}


@responses.activate
def test_create_workflow_bad_response(app):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows",
        json=WORKFLOW_JSON,
        status=500,
    )
    with pytest.raises(ValueError):
        create_workflow(ORGANIZATION_UUID, WORKFLOW_JSON)


@responses.activate
def test_create_workflow_bad_json(app):
    responses.add(
        responses.POST, f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows", body="notjson"
    )
    with pytest.raises(HTTPError):
        create_workflow(ORGANIZATION_UUID, WORKFLOW_JSON)


@responses.activate
def test_create_workflow(app):
    json_response = dict(WORKFLOW_JSON)
    json_response.update(
        {
            "created_at": "2020-10-08T14:22:26.276242",
            "updated_at": "2020-10-08T14:22:26.276278",
            "uuid": "83ac3b4e9433431fbd6d21e7a56b6f0a",
        }
    )
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows",
        json=json_response,
    )
    created_workflow = create_workflow(ORGANIZATION_UUID, WORKFLOW_JSON)
    workflow = OrganizationWorkflow.query.order_by(
        OrganizationWorkflow.id.desc()
    ).first()
    json_response["uuid"] = workflow.uuid
    assert created_workflow == json_response


@responses.activate
def test_fetch_workflows_bad_workflow_responses(app, organization_workflow):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/search",
        status=500,
    )

    with pytest.raises(HTTPError):
        fetch_workflows(ORGANIZATION_UUID)


@responses.activate
def test_fetch_workflows_not_found(app, organization_workflow):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/search",
        json={"error": "not found"},
        status=404,
    )

    with pytest.raises(ValueError):
        fetch_workflows(ORGANIZATION_UUID)


@patch("app.workflows.services.requests.post")
@responses.activate
def test_fetch_workflows_no_workflows(post_mock, app, organization_workflow):
    workflow_list = [
        {"uuid": "12345"},
    ]
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/search",
        json={"uuids": [WORKFLOW_UUID]},
    )
    post_mock().json.return_value = workflow_list

    assert fetch_workflows(ORGANIZATION_UUID) == []
    post_mock.assert_called()
    get_call = post_mock.call_args
    assert get_call[0][0].startswith(app.config[WORKFLOW_HOSTNAME])
    assert get_call[1]["headers"][ROLES_KEY] == app.config[WORKFLOW_API_TOKEN]
    assert get_call[1]["json"] == {"uuids": [organization_workflow.workflow_uuid]}

    post_mock().raise_for_status.assert_called()
    post_mock().json.assert_called()


@responses.activate
def test_fetch_workflow(app, organization_workflow):
    print(organization_workflow)
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{WORKFLOW_UUID}",
        json=WORKFLOW_JSON,
    )

    assert (
        fetch_workflow(ORGANIZATION_UUID, organization_workflow.uuid) == WORKFLOW_JSON
    )


@responses.activate
def test_fetch_workflow_bad_workflow_responses(app, organization_workflow):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{WORKFLOW_UUID}",
        status=500,
    )

    with pytest.raises(HTTPError):
        fetch_workflow(ORGANIZATION_UUID, organization_workflow.uuid)


@responses.activate
def test_fetch_workflow_not_found(app, organization_workflow):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{WORKFLOW_UUID}",
        json={"error": "not found"},
        status=404,
    )

    with pytest.raises(ValueError):
        fetch_workflow(ORGANIZATION_UUID, organization_workflow.uuid)
