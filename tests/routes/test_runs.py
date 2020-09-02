from app.models import db
from app.routes.utils import toISO8601
from app.services import create_pipeline_run
from roles.decorators import ROLES_KEY


def test_create_run_no_such_uuid(client, client_application):
    db.session.commit()
    result = client.post(
        "/v1/pipelines/1111abcd/runs",
        content_type="application/json",
        json={"inputs": []},
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
        json={"inputs": [{"name": "name1.pdf", "url": "aurl", "extrakey": "badinput"}]},
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


def test_create_run(client, pipeline, client_application):
    db.session.commit()
    result = client.post(
        f"/v1/pipelines/{pipeline.uuid}/runs",
        content_type="application/json",
        json={"inputs": [{"name": "name1.pdf", "url": "aurl"}]},
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert len(pipeline.pipeline_runs) == 1
    assert len(pipeline.pipeline_runs[0].pipeline_run_states) == 1
    assert len(pipeline.pipeline_runs[0].pipeline_run_inputs) == 1
    pipeline_run = pipeline.pipeline_runs[0]

    assert result.json == {
        "uuid": pipeline_run.uuid,
        "sequence": pipeline_run.sequence,
        "created_at": toISO8601(pipeline_run.created_at),
        "inputs": [
            {
                "name": "name1.pdf",
                "url": "aurl",
            }
        ],
        "states": [
            {
                "state": pipeline_run.pipeline_run_states[0].name,
                "created_at": toISO8601(pipeline_run.pipeline_run_states[0].created_at),
            }
        ],
    }


def test_get_pipeline_run(client, pipeline, client_application):
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
    pipeline_run = create_pipeline_run(pipeline.uuid, [])
    db.session.commit()
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
    pipeline_run = create_pipeline_run(pipeline.uuid, [])
    db.session.commit()
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
    pipeline_run = create_pipeline_run(pipeline.uuid, [])
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
    pipeline_run = create_pipeline_run(pipeline.uuid, [])
    db.session.commit()

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
