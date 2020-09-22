from unittest.mock import patch

from app.utils import to_iso8601
from app.workflows.models import Workflow, db
from app.workflows.queries import find_workflow
from marshmallow.exceptions import ValidationError
from roles.decorators import ROLES_KEY


@patch("app.workflows.workflow_run_routes.create_workflow_pipeline_run")
def test_start_workflow_run_validation(
    create_run_mock, client, client_application, workflow_pipeline
):
    create_run_mock.side_effect = ValidationError("failure")
    db.session.commit()
    result = client.post(
        f"/v1/workflows/{workflow_pipeline.workflow.uuid}/runs",
        content_type="application/json",
        json={
            "callback_url": "https://example.com",
            "inputs": [],
        },
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400
    assert set(result.json.keys()) == set(["message", "errors"])


@patch("app.workflows.workflow_run_routes.create_workflow_pipeline_run")
def test_start_workflow_run_failure(
    create_run_mock, client, client_application, workflow_pipeline
):
    create_run_mock.side_effect = ValueError("failure")
    db.session.commit()
    result = client.post(
        f"/v1/workflows/{workflow_pipeline.workflow.uuid}/runs",
        content_type="application/json",
        json={
            "callback_url": "https://example.com",
            "inputs": [],
        },
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400
    assert set(result.json.keys()) == set(["message"])


def test_start_workflow(client, client_application, workflow_pipeline):
    db.session.commit()
    result = client.post(
        f"/v1/workflows/{workflow_pipeline.workflow.uuid}/runs",
        content_type="application/json",
        json={
            "callback_url": "https://example.com",
            "inputs": [],
        },
        headers={ROLES_KEY: client_application.api_key},
    )
    workflow_run = workflow_pipeline.workflow.workflow_runs[0]
    workflow_pipeline_run = workflow_run.workflow_pipeline_runs[0]
    pipeline_run = workflow_pipeline_run.pipeline_run
    assert result.status_code == 200
    assert result.json == {
        "uuid": workflow_run.uuid,
        "workflow_pipeline_runs": [
            {
                "uuid": workflow_pipeline_run.uuid,
                "pipeline_run": {
                    "uuid": pipeline_run.uuid,
                    "sequence": pipeline_run.sequence,
                    "inputs": [],
                    "states": [
                        {
                            "created_at": to_iso8601(
                                pipeline_run.pipeline_run_states[0].created_at
                            ),
                            "state": pipeline_run.pipeline_run_states[0].name,
                        }
                    ],
                    "artifacts": [],
                    "created_at": to_iso8601(pipeline_run.created_at),
                },
            }
        ],
        "created_at": to_iso8601(workflow_run.created_at),
        "updated_at": to_iso8601(workflow_run.updated_at),
    }
