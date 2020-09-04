from app.models import db, RunStateEnum, PipelineRunArtifact
from app.routes.utils import toISO8601
from app.services import create_pipeline_run
from app.routes import runs as runs_module
from roles.decorators import ROLES_KEY

from ..test_services import VALID_CALLBACK_INPUT


def test_create_run_no_such_uuid(client, client_application):
    db.session.commit()
    result = client.post(
        "/v1/pipelines/1111abcd/runs",
        content_type="application/json",
        json={"inputs": [], "callback_url": "http://example.com"},
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400


def test_create_run_bad_input_name(client, pipeline, client_application):
    db.session.commit()
    result = client.post(
        f"/v1/pipelines/{pipeline.uuid}/runs",
        content_type="application/json",
        json={"inputs": [{"name": "name1.pdf"}]},
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400

    result = client.post(
        f"/v1/pipelines/{pipeline.uuid}/runs",
        content_type="application/json",
        json={
            "inputs": [
                {
                    "name": "name1.pdf",
                    "url": "http://example.com",
                    "extrakey": "badinput",
                }
            ]
        },
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400

    result = client.post(
        f"/v1/pipelines/{pipeline.uuid}/runs",
        content_type="application/json",
        json={"inputs": "[]"},
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400


def test_create_run_bad_callback_url(client, pipeline, client_application):
    db.session.commit()
    result = client.post(
        f"/v1/pipelines/{pipeline.uuid}/runs",
        content_type="application/json",
        json={
            "inputs": [{"name": "name1.pdf", "url": "http://example.com"}],
            "callback_url": "notaurl",
        },
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400


def test_create_run_bad_input_url(client, pipeline, client_application):
    db.session.commit()
    result = client.post(
        f"/v1/pipelines/{pipeline.uuid}/runs",
        content_type="application/json",
        json={
            "inputs": [{"name": "name1.pdf", "url": "notaurl"}],
            "callback_url": "http://example.com",
        },
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400


def test_create_run(client, pipeline, client_application):
    db.session.commit()
    result = client.post(
        f"/v1/pipelines/{pipeline.uuid}/runs",
        content_type="application/json",
        json={
            "inputs": [{"name": "name1.pdf", "url": "http://example.com"}],
            "callback_url": "http://callback.com",
        },
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert len(pipeline.pipeline_runs) == 1
    assert len(pipeline.pipeline_runs[0].pipeline_run_states) == 1
    assert len(pipeline.pipeline_runs[0].pipeline_run_inputs) == 1
    assert pipeline.pipeline_runs[0].callback_url == "http://callback.com"
    pipeline_run = pipeline.pipeline_runs[0]

    assert result.json == {
        "uuid": pipeline_run.uuid,
        "sequence": pipeline_run.sequence,
        "created_at": toISO8601(pipeline_run.created_at),
        "inputs": [
            {
                "name": "name1.pdf",
                "url": "http://example.com",
            }
        ],
        "states": [
            {
                "state": pipeline_run.pipeline_run_states[0].name,
                "created_at": toISO8601(pipeline_run.pipeline_run_states[0].created_at),
            }
        ],
        "artifacts": [],
    }


def test_get_pipeline_run(client, pipeline, client_application):
    db.session.commit()
    pipeline_run = create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)
    artifact = PipelineRunArtifact(name="test.pdf")
    pipeline_run.pipeline_run_artifacts.append(artifact)
    db.session.commit()

    result = client.get(
        "/v1/pipelines/no-id/runs/no-id",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 404

    # no such pipeline_run_id
    result = client.get(
        f"/v1/pipelines/{pipeline.uuid}/runs/no-id",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 404

    # successfully fetch a pipeline_run
    result = client.get(
        f"/v1/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert result.json == {
        "uuid": pipeline_run.uuid,
        "sequence": pipeline_run.sequence,
        "created_at": toISO8601(pipeline_run.created_at),
        "inputs": [],
        "states": [
            {
                "state": pipeline_run.pipeline_run_states[0].name,
                "created_at": toISO8601(pipeline_run.pipeline_run_states[0].created_at),
            }
        ],
        "artifacts": [
            {
                "uuid": artifact.uuid,
                "name": "test.pdf",
                "url": "",
            }
        ],
    }

    # fails if the pipeline is deleted.
    pipeline.is_deleted = True
    db.session.commit()
    result = client.get(
        f"/v1/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 404


def test_list_pipeline_runs(client, pipeline, client_application):
    db.session.commit()
    result = client.get(
        f"/v1/pipelines/no-id/runs",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 404

    result = client.get(
        f"/v1/pipelines/{pipeline.uuid}/runs",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert result.json == []

    # successfully fetch a pipeline_run
    pipeline_run = create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)
    result = client.get(
        f"/v1/pipelines/{pipeline.uuid}/runs",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert result.json == [
        {
            "uuid": pipeline_run.uuid,
            "sequence": pipeline_run.sequence,
            "created_at": toISO8601(pipeline_run.created_at),
            "inputs": [],
            "states": [
                {
                    "state": pipeline_run.pipeline_run_states[0].name,
                    "created_at": toISO8601(
                        pipeline_run.pipeline_run_states[0].created_at
                    ),
                }
            ],
            "artifacts": [],
        }
    ]


def test_get_pipeline_run_output(client, pipeline, client_application):
    db.session.commit()
    result = client.get(
        "/v1/pipelines/no-id/runs/no-id/console",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 404

    # no such pipeline_run_id
    result = client.get(
        f"/v1/pipelines/{pipeline.uuid}/runs/no-id/console",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 404

    # successfully fetch a pipeline_run
    pipeline_run = create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)
    pipeline_run.std_out = "stdout"
    db.session.commit()
    result = client.get(
        f"/v1/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}/console",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert result.json == {
        "std_out": "stdout",
        "std_err": "",
    }


def test_update_pipeline_run_output(client, pipeline, worker_application):
    db.session.commit()
    pipeline_run = create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)

    result = client.put(
        "/v1/pipelines/no-id/runs/no-id/console",
        content_type="application/json",
        json={
            "std_out": "stdout",
            "std_err": "stderr",
        },
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 404

    # no such pipeline_run_id
    result = client.put(
        f"/v1/pipelines/{pipeline.uuid}/runs/no-id/console",
        content_type="application/json",
        json={
            "std_out": "stdout",
            "std_err": "stderr",
        },
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 404

    # successfully fetch a pipeline_run
    result = client.put(
        f"/v1/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}/console",
        content_type="application/json",
        json={
            "std_out": "stdout",
            "std_err": "stderr",
        },
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 200
    assert pipeline_run.std_out == "stdout"
    assert pipeline_run.std_err == "stderr"


def test_update_pipeline_run_state(client, pipeline, worker_application):
    db.session.commit()
    pipeline_run = create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)

    result = client.put(
        "/v1/pipelines/no-id/runs/no-id/state",
        content_type="application/json",
        json={"state": RunStateEnum.RUNNING.name},
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 404

    # no such pipeline_run_id
    result = client.put(
        f"/v1/pipelines/{pipeline.uuid}/runs/no-id/state",
        content_type="application/json",
        json={"state": RunStateEnum.RUNNING.name},
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 404

    # Bad state
    result = client.put(
        f"/v1/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}/state",
        content_type="application/json",
        json={"state": "badstate"},
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 400

    # Bad state transition
    result = client.put(
        f"/v1/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}/state",
        content_type="application/json",
        json={"state": RunStateEnum.FAILED.name},
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 400

    # successfully fetch a pipeline_run
    result = client.put(
        f"/v1/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}/state",
        content_type="application/json",
        json={"state": RunStateEnum.RUNNING.name},
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 200
    assert len(pipeline_run.pipeline_run_states) == 2
    assert pipeline_run.pipeline_run_states[-1].code == RunStateEnum.RUNNING


def test_upload_run_artifact_service_valueerror(
    client, monkeypatch, pipeline, worker_application
):
    db.session.commit()
    pipeline_run = create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)

    def raise_error(*args, **kwargs):
        raise ValueError("Test error")

    monkeypatch.setattr(runs_module, "create_pipeline_run_artifact", raise_error)

    result = client.post(
        f"/v1/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}/artifacts?name=blah.file",
        data=b"blahblah",
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 400


def test_upload_run_artifact(client, pipeline, worker_application):
    db.session.commit()
    pipeline_run = create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)

    # no 'name' query parameter.
    result = client.post(
        "/v1/pipelines/no-id/runs/no-id/artifacts",
        data=b"blahblah",
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 400

    result = client.post(
        "/v1/pipelines/no-id/runs/no-id/artifacts?name=blah.file",
        data=b"blahblah",
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 404

    # no such pipeline_run_id
    result = client.post(
        f"/v1/pipelines/{pipeline.uuid}/runs/no-id/artifacts?name=blah.file",
        data=b"blahblah",
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 404

    result = client.post(
        f"/v1/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}/artifacts?name=blah.file",
        data=b"blahblah",
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 200
