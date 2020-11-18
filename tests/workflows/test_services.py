from unittest.mock import patch

import pytest
import responses
from app.constants import WORKFLOW_API_TOKEN, WORKFLOW_HOSTNAME
from app.workflows.models import (
    OrganizationWorkflow,
    OrganizationWorkflowPipeline,
)
from app.workflows.services import (
    create_workflow,
    delete_workflow,
    fetch_workflow,
    fetch_workflows,
    update_workflow,
    create_workflow_pipeline,
    fetch_workflow_pipelines,
)
from application_roles.decorators import ROLES_KEY
from requests import HTTPError

from ..conftest import (
    ORGANIZATION_UUID,
    ORGANIZATION_WORKFLOW_PIPELINE_UUID,
    PIPELINE_UUID,
    WORKFLOW_UUID,
    WORKFLOW_PIPELINE_UUID,
    WORKFLOW_PIPELINE_RESPONSE_UUID,
)

WORKFLOW_JSON = {
    "created_at": "2020-11-11T03:19:32.401965",
    "description": "A workflow that does cool things2",
    "name": "My Workflow",
    "updated_at": "2020-11-11T03:19:32.401973",
    "uuid": WORKFLOW_UUID,
}
ORGANIZATION_WORKFLOW_PIPELINE_RESPONSE_JSON = {
    "created_at": "2020-11-11T03:19:32.401965",
    "updated_at": "2020-11-11T03:19:32.401973",
    "pipeline_uuid": ORGANIZATION_WORKFLOW_PIPELINE_UUID,
    "source_workflow_pipelines": [WORKFLOW_PIPELINE_UUID],
    "destination_workflow_pipelines": [WORKFLOW_PIPELINE_UUID],
    "uuid": WORKFLOW_PIPELINE_RESPONSE_UUID,
}
WORKFLOW_PIPELINE_RESPONSE_JSON = {
    "created_at": "2020-11-11T03:19:32.401965",
    "updated_at": "2020-11-11T03:19:32.401973",
    "pipeline_uuid": PIPELINE_UUID,
    "source_workflow_pipelines": [WORKFLOW_PIPELINE_UUID],
    "destination_workflow_pipelines": [WORKFLOW_PIPELINE_UUID],
    "uuid": WORKFLOW_PIPELINE_UUID,
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
    json_response = WORKFLOW_JSON
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{WORKFLOW_UUID}",
        json=WORKFLOW_JSON,
    )

    json_response["uuid"] = organization_workflow.uuid

    assert (
        fetch_workflow(ORGANIZATION_UUID, organization_workflow.uuid) == WORKFLOW_JSON
    )


@responses.activate
def test_fetch_workflow_missing_workflow(app, organization_workflow):
    with pytest.raises(ValueError):
        fetch_workflow("12345", organization_workflow.uuid)


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


@responses.activate
def test_update_workflow(app, organization_workflow):
    updates = {"name": "123", "description": "456"}
    json_response = dict(WORKFLOW_JSON)
    json_response.update(updates)

    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{WORKFLOW_UUID}",
        json=json_response,
    )
    updated_workflow = update_workflow(
        ORGANIZATION_UUID, organization_workflow.uuid, updates
    )

    json_response["uuid"] = organization_workflow.uuid
    assert updated_workflow == json_response


@responses.activate
def test_update_workflow_invalid_org_missing_params(app, organization_workflow):
    with pytest.raises(ValueError):
        update_workflow("1234", organization_workflow.uuid, {})

    with pytest.raises(ValueError):
        update_workflow(
            ORGANIZATION_UUID, organization_workflow.uuid, {"missing": "params"}
        )


@responses.activate
def test_update_workflow_bad_workflow_responses(app, organization_workflow):
    updates = {"name": "123", "description": "456"}
    json_response = dict(WORKFLOW_JSON)
    json_response.update(updates)

    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{WORKFLOW_UUID}",
        status=500,
    )

    with pytest.raises(HTTPError):
        update_workflow(ORGANIZATION_UUID, organization_workflow.uuid, updates)


@responses.activate
def test_update_workflow_not_found(app, organization_workflow):
    updates = {"name": "123", "description": "456"}
    json_response = dict(WORKFLOW_JSON)
    json_response.update(updates)

    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{WORKFLOW_UUID}",
        json={"error": "not found"},
        status=404,
    )

    with pytest.raises(ValueError):
        update_workflow(ORGANIZATION_UUID, organization_workflow.uuid, updates)


def test_delete_workflow_not_found(app, organization_workflow):
    with pytest.raises(ValueError):
        delete_workflow(ORGANIZATION_UUID, "1234")


@responses.activate
def test_delete_workflow_not_found_workflow(app, organization_workflow):
    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}",
        json={"error": "not found"},
        status=404,
    )

    with pytest.raises(HTTPError):
        delete_workflow(ORGANIZATION_UUID, organization_workflow.uuid)


@responses.activate
def test_delete_workflow(app, organization_workflow):
    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}",
        json={},
        status=200,
    )

    delete_workflow(ORGANIZATION_UUID, organization_workflow.uuid)

    org_workflow = OrganizationWorkflow.query.filter(
        OrganizationWorkflow.uuid == organization_workflow.uuid
    ).one()

    assert org_workflow.is_deleted


def test_create_workflow_pipeline_invalid_org_workflow(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    with pytest.raises(ValueError):
        create_workflow_pipeline(organization_workflow.organization_uuid, "1234", {})


def test_create_workflow_pipeline_invalid_org_pipeline(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    with pytest.raises(ValueError):
        create_workflow_pipeline(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            {
                "pipeline_uuid": "1234",
            },
        )


@responses.activate
def test_create_workflow_pipeline_bad_json(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}/pipelines",
        body="notjson",
        status=503,
    )

    with pytest.raises(HTTPError):
        create_workflow_pipeline(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            {
                "pipeline_uuid": organization_pipeline.uuid,
            },
        )


@responses.activate
def test_create_workflow_pipeline_not_found(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}/pipelines",
        json={"not": "found"},
        status=404,
    )

    with pytest.raises(ValueError):
        create_workflow_pipeline(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            {
                "pipeline_uuid": organization_pipeline.uuid,
                "source_workflow_pipelines": [],
                "destination_workflow_pipelines": [],
            },
        )


@responses.activate
def test_create_workflow(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}/pipelines",
        json=ORGANIZATION_WORKFLOW_PIPELINE_RESPONSE_JSON,
    )

    new_org_workflow_pipeline = create_workflow_pipeline(
        organization_workflow.organization_uuid,
        organization_workflow.uuid,
        {
            "pipeline_uuid": organization_pipeline.uuid,
            "source_workflow_pipelines": [
                organization_workflow_pipeline.uuid,
            ],
            "destination_workflow_pipelines": [
                organization_workflow_pipeline.uuid,
            ],
        },
    )

    created_org_workflow_pipeline = OrganizationWorkflowPipeline.query.filter(
        OrganizationWorkflowPipeline.uuid == new_org_workflow_pipeline.get("uuid")
    ).first()

    assert created_org_workflow_pipeline is not None
    assert (
        created_org_workflow_pipeline.organization_pipeline_id
        == organization_pipeline.id
    )


def test_fetch_workflow_pipelines_invalid_org_workflow(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    with pytest.raises(ValueError):
        fetch_workflow_pipelines(organization_workflow.organization_uuid, "1234")


def test_create_workflow_pipeline_invalid_org_pipeline(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    with pytest.raises(ValueError):
        create_workflow_pipeline(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            {
                "pipeline_uuid": "1234",
            },
        )


@responses.activate
def test_fetch_workflow_pipelines_bad_json(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}/pipelines",
        body="notjson",
        status=503,
    )

    with pytest.raises(HTTPError):
        fetch_workflow_pipelines(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
        )


@responses.activate
def test_fetch_workflow_pipelines_not_found(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}/pipelines",
        json={"not": "found"},
        status=404,
    )

    with pytest.raises(ValueError):
        fetch_workflow_pipelines(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
        )


@responses.activate
def test_fetch_workflow_pipelines(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}/pipelines",
        json=[WORKFLOW_PIPELINE_RESPONSE_JSON],
    )

    org_workflow_pipelines = fetch_workflow_pipelines(
        organization_workflow.organization_uuid,
        organization_workflow.uuid,
    )

    first_result = org_workflow_pipelines[0]

    assert first_result["uuid"] == organization_workflow_pipeline.uuid
    assert first_result["source_workflow_pipelines"] == [
        organization_workflow_pipeline.uuid
    ]
    assert first_result["destination_workflow_pipelines"] == [
        organization_workflow_pipeline.uuid
    ]
