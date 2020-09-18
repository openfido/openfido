from unittest.mock import patch

from roles.decorators import ROLES_KEY
from app.workflows.models import db, Workflow
from app.utils import to_iso8601
from app.workflows.queries import find_workflow_pipeline
from app.workflows.services import create_workflow_pipeline


@patch("app.workflows.workflow_pipeline_routes.create_workflow_pipeline")
def test_create_workflow_pipeline_failure(
    create_workflow_pipeline_mock, client, client_application, workflow
):
    create_workflow_pipeline_mock.side_effect = ValueError("failure")
    db.session.commit()
    result = client.post(
        f"/v1/workflows/{workflow.uuid}/pipelines",
        content_type="application/json",
        json={},
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400
    assert set(result.json.keys()) == set(["message"])


def test_create_workflow_pipeline_bad_input(client, client_application, workflow):
    result = client.post(
        f"/v1/workflows/{workflow.uuid}/pipelines",
        content_type="application/json",
        json={},
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400


def test_create_workflow_pipeline(
    client, client_application, pipeline, workflow, workflow_pipeline
):
    another_workflow_pipeline = create_workflow_pipeline(
        workflow.uuid,
        {
            "pipeline_uuid": pipeline.uuid,
            "source_workflow_pipelines": [],
            "destination_workflow_pipelines": [],
        },
    )
    params = {
        "pipeline_uuid": pipeline.uuid,
        "source_workflow_pipelines": [workflow_pipeline.uuid],
        "destination_workflow_pipelines": [another_workflow_pipeline.uuid],
    }
    result = client.post(
        f"/v1/workflows/{workflow.uuid}/pipelines",
        content_type="application/json",
        json=params,
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    workflow_pipeline = find_workflow_pipeline(result.json["uuid"])
    assert result.json == {
        "uuid": workflow_pipeline.uuid,
        "pipeline_uuid": pipeline.uuid,
        "source_workflow_pipelines": [workflow_pipeline.uuid],
        "destination_workflow_pipelines": [another_workflow_pipeline.uuid],
        "created_at": to_iso8601(workflow_pipeline.created_at),
        "updated_at": to_iso8601(workflow_pipeline.updated_at),
    }
