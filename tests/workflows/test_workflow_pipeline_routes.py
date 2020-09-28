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


def test_get_workflow_pipelines_404(
    client, client_application, pipeline, workflow, workflow_pipeline
):
    db.session.commit()
    result = client.get(
        f"/v1/workflows/{workflow.uuid}/pipelines/{'0' * 32}",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 404

    result = client.get(
        f"/v1/workflows/{'0' * 32}/pipelines/{'0' * 32}",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 404


def test_get_workflow_pipelines(
    client, client_application, pipeline, workflow, workflow_pipeline
):
    db.session.commit()
    result = client.get(
        f"/v1/workflows/{workflow.uuid}/pipelines/{workflow_pipeline.uuid}",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert result.json == {
        "uuid": workflow_pipeline.uuid,
        "pipeline_uuid": pipeline.uuid,
        "source_workflow_pipelines": [],
        "destination_workflow_pipelines": [],
        "created_at": to_iso8601(workflow_pipeline.created_at),
        "updated_at": to_iso8601(workflow_pipeline.updated_at),
    }


def test_list_workflow_pipelines_404(client, client_application, pipeline, workflow):
    db.session.commit()
    result = client.get(
        f"/v1/workflows/{'0' * 32}/pipelines",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 404


def test_list_workflow_pipelines(client, client_application, pipeline, workflow):
    db.session.commit()
    result = client.get(
        f"/v1/workflows/{workflow.uuid}/pipelines",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert len(result.json) == 0

    wp1 = create_workflow_pipeline(
        workflow.uuid,
        {
            "pipeline_uuid": pipeline.uuid,
            "source_workflow_pipelines": [],
            "destination_workflow_pipelines": [],
        },
    )

    wp2 = create_workflow_pipeline(
        workflow.uuid,
        {
            "pipeline_uuid": pipeline.uuid,
            "source_workflow_pipelines": [],
            "destination_workflow_pipelines": [],
        },
    )

    result = client.get(
        f"/v1/workflows/{workflow.uuid}/pipelines",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert len(result.json) == 2
    assert result.json[0]["uuid"] == wp1.uuid
    assert result.json[1]["uuid"] == wp2.uuid


def test_delete_workflow_pipeline(
    client, client_application, pipeline, workflow, workflow_pipeline
):
    db.session.commit()
    result = client.delete(
        f"/v1/workflows/{workflow.uuid}/pipelines/{workflow_pipeline.uuid}",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert len(result.json) == 0
    assert find_workflow_pipeline(workflow_pipeline.uuid) is None


@patch("app.workflows.workflow_pipeline_routes.delete_workflow_pipeline")
def test_delete_workflow_pipeline_error(
    delete_mock, client, client_application, pipeline, workflow, workflow_pipeline
):
    delete_mock.side_effect = ValueError("something went wrong")
    db.session.commit()
    result = client.delete(
        f"/v1/workflows/{workflow.uuid}/pipelines/{workflow_pipeline.uuid}",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400
