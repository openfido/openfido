import copy

from marshmallow.exceptions import ValidationError
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
    fetch_workflow_pipeline,
    update_workflow_pipeline,
    delete_workflow_pipeline,
    create_workflow_run,
    fetch_workflow_run,
)
from application_roles.decorators import ROLES_KEY
from requests import HTTPError

from ..conftest import (
    ORGANIZATION_UUID,
    ORGANIZATION_WORKFLOW_PIPELINE_UUID,
    PIPELINE_UUID,
    PIPELINE_RUN_UUID,
    WORKFLOW_UUID,
    WORKFLOW_PIPELINE_UUID,
    WORKFLOW_PIPELINE_RESPONSE_UUID,
    ORGANIZATION_WORKFLOW_RUN_UUID,
    ORGANIZATION_WORKFLOW_PIPELINE_RUN_UUID,
    WORKFLOW_RUN_UUID,
    WORKFLOW_PIPELINE_RUN_UUID,
)

from ..pipelines.test_services import (
    PIPELINE_RUN_RESPONSE_JSON,
    PIPELINE_RUN_INPUT_FILE_JSON,
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
WORKFLOW_PIPELINE_RUN_RESPONSE_JSON = {
    "uuid": WORKFLOW_PIPELINE_RUN_UUID,
    "created_at": "2020-08-05T08:15:30-05:00",
    "status": "NOT_STARTED",
    "workflow_pipeline_runs": [
        {
            "uuid": WORKFLOW_RUN_UUID,
            "pipeline_run": {
                "uuid": PIPELINE_RUN_UUID,
                "sequence": 1,
                "created_at": "2020-08-05T08:15:30-05:00",
                "inputs": [
                    {"uuid": "abc123", "name": "file.csv", "url": "https://myfile"},
                    {"uuid": "abc123", "name": "file.csv", "url": "https://myfile"},
                ],
                "states": [
                    {"state": "NOT_STARTED", "created_at": "2020-08-05T08:15:30-05:00"}
                ],
            },
        }
    ],
}

ORGANIZATION_WORKFLOW_RUN_RESPONSE = {
    "uuid": "c4e16220c35547d8bb1734e443f05ef4",
    "created_at": "2020-08-05T08:15:30-05:00",
    "status": "NOT_STARTED",
    "workflow_pipeline_runs": [
        {
            "uuid": "de24e7e32aed48719e313911509353a2",
            "pipeline_run": {
                "created_at": "2020-10-28T22:01:48.950370",
                "inputs": [
                    {
                        "name": "00000000000000000000000000000000organization_pipeline_input_file.csv",
                        "url": "http://somefileurl.com",
                        "uuid": "1a393d3d847d41b4bbf006738bb576c5",
                    }
                ],
                "sequence": 1,
                "states": [
                    {"created_at": "2020-10-28T22:01:48.951140", "state": "QUEUED"},
                    {
                        "created_at": "2020-10-28T22:01:48.955688",
                        "state": "NOT_STARTED",
                    },
                    [{"created_at": "2020-10-28T22:02:48.955688", "state": "RUNNING"}],
                    [
                        {
                            "created_at": "2020-10-28T22:03:48.955688",
                            "state": "COMPLETED",
                        }
                    ],
                ],
                "uuid": "d6c42c749a1643aba0217c02e177625f",
            },
        }
    ],
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
    with pytest.raises(ValidationError):
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
    with pytest.raises(ValidationError):
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
                "pipeline_uuid": "1" * 32,
                "destination_workflow_pipelines": [],
                "source_workflow_pipelines": [],
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


def test_fetch_workflow_pipeline_invalid_org_workflow(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    with pytest.raises(ValueError):
        fetch_workflow_pipeline(
            organization_workflow.organization_uuid,
            "1234",
            organization_workflow_pipeline.uuid,
        )


def test_fetch_workflow_pipeline_invalid_org_pipeline(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    with pytest.raises(ValueError):
        fetch_workflow_pipeline(
            organization_workflow.organization_uuid, organization_workflow.uuid, "1234"
        )


@responses.activate
def test_fetch_workflow_pipeline_bad_json(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/pipelines/{wf_pipeline_uuid}",
        body="notjson",
        status=503,
    )

    with pytest.raises(HTTPError):
        fetch_workflow_pipeline(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            organization_workflow_pipeline.uuid,
        )


@responses.activate
def test_fetch_workflow_pipeline_not_found(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/pipelines/{wf_pipeline_uuid}",
        json={"not": "found"},
        status=404,
    )

    with pytest.raises(ValueError):
        fetch_workflow_pipeline(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            organization_workflow_pipeline.uuid,
        )


@responses.activate
def test_fetch_workflow_pipeline(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/pipelines/{wf_pipeline_uuid}",
        json=WORKFLOW_PIPELINE_RESPONSE_JSON,
    )

    wf_pipeline = fetch_workflow_pipeline(
        organization_workflow.organization_uuid,
        organization_workflow.uuid,
        organization_workflow_pipeline.uuid,
    )

    assert wf_pipeline.get("uuid") == organization_workflow_pipeline.uuid
    assert wf_pipeline.get("pipeline_uuid") == organization_pipeline.uuid
    assert organization_workflow_pipeline.uuid in wf_pipeline.get(
        "source_workflow_pipelines"
    )
    assert organization_workflow_pipeline.uuid in wf_pipeline.get(
        "destination_workflow_pipelines"
    )


def test_update_workflow_pipeline_invalid_org_workflow(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    with pytest.raises(ValueError):
        update_workflow_pipeline(
            organization_workflow.organization_uuid,
            "1234",
            organization_workflow_pipeline.uuid,
            {
                "pipeline_uuid": organization_pipeline.pipeline_uuid,
                "destination_workflow_pipelines": [],
                "source_workflow_pipelines": [],
            },
        )


def test_update_workflow_pipeline_invalid_org_pipeline(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    with pytest.raises(ValueError):
        update_workflow_pipeline(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            organization_workflow_pipeline.uuid,
            {
                "pipeline_uuid": organization_pipeline.pipeline_uuid,
                "destination_workflow_pipelines": [],
                "source_workflow_pipelines": [],
            },
        )


def test_update_workflow_pipeline_invalid_org_workflow_pipeline(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    with pytest.raises(ValueError):
        update_workflow_pipeline(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            "1234",
            {
                "pipeline_uuid": organization_pipeline.uuid,
                "destination_workflow_pipelines": [],
                "source_workflow_pipelines": [],
            },
        )


@responses.activate
def test_update_workflow_pipeline_bad_json(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/pipelines/{wf_pipeline_uuid}",
        body="notjson",
        status=503,
    )

    with pytest.raises(HTTPError):
        update_workflow_pipeline(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            organization_workflow_pipeline.uuid,
            {
                "source_workflow_pipelines": [
                    organization_workflow_pipeline.uuid,
                ],
                "pipeline_uuid": organization_pipeline.uuid,
                "destination_workflow_pipelines": [
                    organization_workflow_pipeline.uuid,
                ],
            },
        )


@responses.activate
def test_update_workflow_pipeline_not_found(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/pipelines/{wf_pipeline_uuid}",
        json={"not": "found"},
        status=404,
    )

    with pytest.raises(ValueError):
        update_workflow_pipeline(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            organization_workflow_pipeline.uuid,
            {
                "source_workflow_pipelines": [
                    organization_workflow_pipeline.uuid,
                ],
                "pipeline_uuid": organization_pipeline.uuid,
                "destination_workflow_pipelines": [
                    organization_workflow_pipeline.uuid,
                ],
            },
        )


@responses.activate
def test_update_workflow_pipeline(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    mock_response = copy.deepcopy(WORKFLOW_PIPELINE_RESPONSE_JSON)
    mock_response["source_workflow_pipelines"].append(
        organization_workflow_pipeline.uuid
    )
    mock_response["destination_workflow_pipelines"].append(
        organization_workflow_pipeline.uuid
    )

    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/pipelines/{wf_pipeline_uuid}",
        json=mock_response,
    )

    update_wf_pipeline = update_workflow_pipeline(
        organization_workflow.organization_uuid,
        organization_workflow.uuid,
        organization_workflow_pipeline.uuid,
        {
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

    assert update_wf_pipeline.get("uuid") == organization_workflow_pipeline.uuid
    assert update_wf_pipeline.get("pipeline_uuid") == organization_pipeline.uuid

    for key in ["source_workflow_pipelines", "destination_workflow_pipelines"]:
        assert all(
            ow_p == organization_workflow_pipeline.uuid
            for ow_p in update_wf_pipeline[key]
        )


def test_delete_workflow_pipeline_invalid_org_workflow(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    with pytest.raises(ValueError):
        delete_workflow_pipeline(
            organization_workflow.organization_uuid,
            "1234",
            organization_workflow_pipeline.uuid,
        )


def test_delete_workflow_pipeline_invalid_org_workflow_pipeline(
    app, organization_workflow, organization_pipeline, organization_workflow_pipeline
):
    with pytest.raises(ValueError):
        delete_workflow_pipeline(
            organization_workflow.organization_uuid, organization_workflow.uuid, "1234"
        )


@responses.activate
def test_delete_workflow_pipeline_bad_json(
    app, organization_workflow, organization_workflow_pipeline
):
    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/pipelines/{wf_pipeline_uuid}",
        body="notjson",
        status=503,
    )

    with pytest.raises(HTTPError):
        delete_workflow_pipeline(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            organization_workflow_pipeline.uuid,
        )


@responses.activate
def test_delete_workflow_pipeline_not_found(
    app, organization_workflow, organization_workflow_pipeline
):
    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/pipelines/{wf_pipeline_uuid}",
        json={"not": "found"},
        status=404,
    )

    with pytest.raises(HTTPError):
        delete_workflow_pipeline(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            organization_workflow_pipeline.uuid,
        )


@responses.activate
def test_delete_workflow_pipeline(
    app, organization_workflow, organization_workflow_pipeline
):
    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/pipelines/{wf_pipeline_uuid}",
        status=204,
    )

    delete_workflow_pipeline(
        organization_workflow.organization_uuid,
        organization_workflow.uuid,
        organization_workflow_pipeline.uuid,
    )

    ow_pipeline = OrganizationWorkflowPipeline.query.filter(
        OrganizationWorkflowPipeline.uuid == organization_workflow_pipeline.uuid
    ).first()

    assert ow_pipeline.is_deleted is True


def test_create_workflow_run_invalid_org_workflow(app, organization_workflow):
    with pytest.raises(ValueError):
        create_workflow_run(
            organization_workflow.organization_uuid,
            "1234",
            PIPELINE_RUN_INPUT_FILE_JSON,
        )


def test_create_workflow_run_invalid_no_pipelines(
    app, organization_workflow, monkeypatch
):
    monkeypatch.setattr(OrganizationWorkflow, "organization_workflow_pipelines", [])

    with pytest.raises(ValueError):
        create_workflow_run(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            PIPELINE_RUN_INPUT_FILE_JSON,
        )


@responses.activate
def test_create_workflow_run_bad_json(
    app, organization_workflow, organization_workflow_pipeline
):
    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/runs",
        body="notjson",
        status=503,
    )

    with pytest.raises(HTTPError):
        create_workflow_run(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            PIPELINE_RUN_INPUT_FILE_JSON,
        )


@responses.activate
def test_create_workflow_run_not_found(
    app, organization_workflow, organization_workflow_pipeline
):
    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/runs",
        json={"not": "found"},
        status=404,
    )

    with pytest.raises(ValueError):
        create_workflow_run(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            PIPELINE_RUN_INPUT_FILE_JSON,
        )


@patch("app.workflows.services.create_url")
@patch("app.workflows.services.fetch_pipeline_run")
@responses.activate
def test_create_workflow_run(
    mock_fetch_pipeline_run,
    mock_url,
    app,
    organization_workflow,
    organization_workflow_pipeline,
    organization_pipeline_run,
    organization_pipeline,
    organization_pipeline_input_file,
    organization_workflow_run,
    organization_workflow_pipeline_run,
):
    mock_fetch_pipeline_run.return_value = dict(PIPELINE_RUN_RESPONSE_JSON)
    mock_url.return_value = "http://somefileurl.com"

    wf_uuid = organization_workflow.workflow_uuid
    wf_pipeline_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/runs",
        json=WORKFLOW_PIPELINE_RUN_RESPONSE_JSON,
        status=200,
    )

    new_org_workflow_run = create_workflow_run(
        organization_workflow.organization_uuid,
        organization_workflow.uuid,
        PIPELINE_RUN_INPUT_FILE_JSON,
    )

    # update to use newly created uuids
    org_wf_run_uuid = new_org_workflow_run["workflow_pipeline_runs"][0]["uuid"]
    ORGANIZATION_WORKFLOW_RUN_RESPONSE["uuid"] = new_org_workflow_run["uuid"]
    ORGANIZATION_WORKFLOW_RUN_RESPONSE["created_at"] = new_org_workflow_run[
        "created_at"
    ]
    ORGANIZATION_WORKFLOW_RUN_RESPONSE["workflow_pipeline_runs"][0][
        "uuid"
    ] = org_wf_run_uuid

    assert new_org_workflow_run == ORGANIZATION_WORKFLOW_RUN_RESPONSE


def test_workflow_run_invalid_org_workflow(
    app, organization_workflow, organization_workflow_run
):
    with pytest.raises(ValueError):
        fetch_workflow_run(
            organization_workflow.organization_uuid, organization_workflow.uuid, "1234"
        )


@responses.activate
def test_workflow_run_bad_json(
    app,
    organization_workflow,
    organization_workflow_pipeline,
    organization_workflow_run,
):
    wf_uuid = organization_workflow.workflow_uuid
    wfr_uuid = organization_workflow_run.workflow_run_uuid

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/runs/{wfr_uuid}",
        body="notjson",
        status=503,
    )

    with pytest.raises(HTTPError):
        fetch_workflow_run(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            organization_workflow_run.uuid,
        )


@responses.activate
def test_workflow_run_not_found(
    app,
    organization_workflow,
    organization_workflow_pipeline,
    organization_workflow_run,
):
    wf_uuid = organization_workflow.workflow_uuid
    wfr_uuid = organization_workflow_run.workflow_run_uuid

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/runs/{wfr_uuid}",
        json={"not": "found"},
        status=404,
    )

    with pytest.raises(ValueError):
        fetch_workflow_run(
            organization_workflow.organization_uuid,
            organization_workflow.uuid,
            organization_workflow_run.uuid,
        )


@patch("app.workflows.services.create_url")
@patch("app.workflows.services.fetch_pipeline_run")
@responses.activate
def test_fetch_workflow_run(
    mock_fetch_pipeline_run,
    mock_url,
    app,
    organization_workflow,
    organization_workflow_pipeline,
    organization_pipeline_run,
    organization_pipeline,
    organization_pipeline_input_file,
    organization_workflow_run,
    organization_workflow_pipeline_run,
):
    mock_fetch_pipeline_run.return_value = dict(PIPELINE_RUN_RESPONSE_JSON)
    mock_url.return_value = "http://somefileurl.com"

    wf_uuid = organization_workflow.workflow_uuid
    wfr_uuid = organization_workflow_run.workflow_run_uuid

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{wf_uuid}/runs/{wfr_uuid}",
        json=WORKFLOW_PIPELINE_RUN_RESPONSE_JSON,
        status=200,
    )

    org_workflow_run = fetch_workflow_run(
        organization_workflow.organization_uuid,
        organization_workflow.uuid,
        organization_workflow_run.uuid,
    )

    org_wf_run_uuid = org_workflow_run["workflow_pipeline_runs"][0]["uuid"]
    ORGANIZATION_WORKFLOW_RUN_RESPONSE["uuid"] = organization_workflow_run.uuid
    ORGANIZATION_WORKFLOW_RUN_RESPONSE["workflow_pipeline_runs"][0][
        "uuid"
    ] = organization_workflow_run.uuid

    assert org_workflow_run == ORGANIZATION_WORKFLOW_RUN_RESPONSE
