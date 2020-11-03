import io
import json
from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest
from marshmallow.exceptions import ValidationError

from app.constants import S3_BUCKET, CALLBACK_TIMEOUT
from app.model_utils import RunStateEnum
from app.pipelines import services
from app.pipelines.models import db, PipelineRunArtifact
from app.pipelines.queries import find_pipeline

A_NAME = "a pipeline"
A_DESCRIPTION = "a description"
A_DOCKER_IMAGE = "example/image"
A_SSH_URL = "git@github.com:an_org/a_repo.git"
A_BRANCH = "master"

INVALID_CALLBACK_INPUT = {"inputs": [], "callback_url": "notaurl"}
VALID_CALLBACK_INPUT = {"inputs": [], "callback_url": "http://example.com"}


def test_create_pipeline_version_no_name(app):
    # Can't create a pipeline without some kind of URL configuration.
    with pytest.raises(ValueError):
        services.create_pipeline("", A_DESCRIPTION, A_DOCKER_IMAGE, A_SSH_URL, A_BRANCH)


def test_create_pipeline_version_no_docker(app):
    # Can't create a pipeline without some kind of URL configuration.
    with pytest.raises(ValueError):
        services.create_pipeline(A_NAME, A_DESCRIPTION, "", "", "")


def test_create_pipeline_version_no_ssh_url(app):
    # Can't create a pipeline without some kind of URL configuration.
    with pytest.raises(ValueError):
        services.create_pipeline(A_NAME, A_DESCRIPTION, A_DOCKER_IMAGE, "", "")


def test_create_pipeline(app):
    pipeline = services.create_pipeline(
        A_NAME, A_DESCRIPTION, A_DOCKER_IMAGE, A_SSH_URL, A_BRANCH
    )
    assert pipeline.name == A_NAME
    assert pipeline.description == A_DESCRIPTION
    assert pipeline.docker_image_url == A_DOCKER_IMAGE
    assert pipeline.repository_ssh_url == A_SSH_URL
    assert pipeline.repository_branch == A_BRANCH


def test_update_pipeline_no_uuid(app):
    with pytest.raises(ValueError):
        services.update_pipeline(
            "baduuid", A_NAME, A_DESCRIPTION, A_DOCKER_IMAGE, A_SSH_URL, A_BRANCH
        )


def test_update_pipeline(app, pipeline):
    pipeline = services.update_pipeline(
        pipeline.uuid, A_NAME, A_DESCRIPTION, A_DOCKER_IMAGE, A_SSH_URL, A_BRANCH
    )
    assert pipeline.name == A_NAME
    assert pipeline.description == A_DESCRIPTION
    assert pipeline.docker_image_url == A_DOCKER_IMAGE
    assert pipeline.repository_ssh_url == A_SSH_URL
    assert pipeline.repository_branch == A_BRANCH


def test_delete_pipeline_no_record(app):
    with pytest.raises(ValueError):
        services.delete_pipeline("fake-id")


def test_delete_pipeline(app, pipeline):
    services.delete_pipeline(pipeline.uuid)

    assert pipeline.is_deleted


def test_delete_pipeline_has_workflow(app, pipeline, workflow, workflow_pipeline):
    with pytest.raises(ValueError):
        services.delete_pipeline(pipeline.uuid)

    assert not pipeline.is_deleted


def test_create_pipeline_bad_input(app):
    with pytest.raises(ValidationError):
        pipeline_run = services.create_pipeline_run("no-id", INVALID_CALLBACK_INPUT)


def test_create_pipeline_run_no_pipeline(app):
    with pytest.raises(ValueError):
        pipeline_run = services.create_pipeline_run("no-id", VALID_CALLBACK_INPUT)


def test_start_pipeline_run_bad_state(app, pipeline):
    pipeline_run = services.create_pipeline_run(
        pipeline.uuid,
        {"inputs": [], "callback_url": "http://example.com"},
    )
    with pytest.raises(ValueError):
        services.start_pipeline_run(pipeline_run)


def test_create_pipeline_run(app, pipeline, mock_execute_pipeline):
    input1 = {
        "name": "name1.pdf",
        "url": "https://example.com/name1.pdf",
    }
    input2 = {
        "name": "name2.pdf",
        "url": "https://example.com/name2.pdf",
    }
    pipeline_run = services.create_pipeline_run(
        pipeline.uuid,
        {"inputs": [input1, input2], "callback_url": "http://example.com"},
    )
    assert pipeline_run.pipeline == pipeline
    assert pipeline_run.sequence == 1
    assert len(pipeline_run.pipeline_run_inputs) == 2
    assert pipeline_run.pipeline_run_inputs[0].filename == input1["name"]
    assert pipeline_run.pipeline_run_inputs[1].filename == input2["name"]
    assert len(pipeline_run.pipeline_run_states) == 2
    assert pipeline_run.pipeline_run_states[0].code == RunStateEnum.QUEUED
    assert pipeline_run.pipeline_run_states[1].code == RunStateEnum.NOT_STARTED


def test_create_queued_pipeline_run(app, pipeline):
    input1 = {
        "name": "name1.pdf",
        "url": "https://example.com/name1.pdf",
    }
    input2 = {
        "name": "name2.pdf",
        "url": "https://example.com/name2.pdf",
    }
    pipeline_run = services.create_pipeline_run(
        pipeline.uuid,
        {"inputs": [input1, input2], "callback_url": "http://example.com"},
        True,
    )
    assert pipeline_run.pipeline == pipeline
    assert pipeline_run.sequence == 1
    assert len(pipeline_run.pipeline_run_inputs) == 2
    assert pipeline_run.pipeline_run_inputs[0].filename == input1["name"]
    assert pipeline_run.pipeline_run_inputs[1].filename == input2["name"]
    assert len(pipeline_run.pipeline_run_states) == 1
    assert pipeline_run.pipeline_run_states[0].code == RunStateEnum.QUEUED


def test_update_pipeline_run_output_no_uuid(app, pipeline):
    with pytest.raises(ValueError):
        services.update_pipeline_run_output(None, "stdout", "stderr")


def test_update_pipeline_run_output(app, pipeline, mock_execute_pipeline):
    pipeline_run = services.create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)

    services.update_pipeline_run_output(pipeline_run.uuid, "stdout", "stderr")
    assert pipeline_run.std_out == "stdout"
    assert pipeline_run.std_err == "stderr"


def test_update_pipeline_run_state_bad_state(app, pipeline, mock_execute_pipeline):
    pipeline_run = services.create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)

    with pytest.raises(ValidationError):
        services.update_pipeline_run_state(
            pipeline_run.uuid,
            {
                "state": "fake",
            },
        )

    assert len(pipeline_run.pipeline_run_states) == 2


def test_update_pipeline_run_state_dup_state(app, pipeline, mock_execute_pipeline):
    pipeline_run = services.create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)

    with pytest.raises(ValueError):
        services.update_pipeline_run_state(
            pipeline_run.uuid,
            {
                "state": RunStateEnum.NOT_STARTED.name,
            },
        )
    assert len(pipeline_run.pipeline_run_states) == 2


def test_update_pipeline_run_state_bad_transition(app, pipeline, mock_execute_pipeline):
    pipeline_run = services.create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)

    with pytest.raises(ValueError):
        services.update_pipeline_run_state(
            pipeline_run.uuid,
            {
                "state": RunStateEnum.COMPLETED.name,
            },
        )
    assert len(pipeline_run.pipeline_run_states) == 2


def test_update_pipeline_run_state_callback_err(
    app, monkeypatch, pipeline, mock_execute_pipeline
):
    pipeline_run = services.create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)

    # If a callback_url fails for some network reason, the update should still
    # work:
    def mock_urlopen(request, timeout):
        raise URLError("a reason")

    monkeypatch.setattr(services.urllib_request, "urlopen", mock_urlopen)

    services.update_pipeline_run_state(
        pipeline_run.uuid,
        {
            "state": RunStateEnum.RUNNING.name,
        },
    )
    assert len(pipeline_run.pipeline_run_states) == 3
    assert pipeline_run.run_state_enum() == RunStateEnum.RUNNING


def test_update_pipeline_run_state_no_pipeline(app):
    with pytest.raises(ValueError):
        services.update_pipeline_run_state(
            "nosuchid",
            {
                "state": RunStateEnum.RUNNING.name,
            },
        )


def test_update_pipeline_run_state(app, monkeypatch, pipeline, mock_execute_pipeline):
    pipeline_run = services.create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)

    # A callback is made with the callback_url and the correct payload
    def mock_urlopen(request, timeout):
        assert request.full_url == pipeline_run.callback_url
        assert json.loads(request.data.decode()) == {
            "pipeline_run_uuid": pipeline_run.uuid,
            "state": RunStateEnum.RUNNING.name,
        }
        assert timeout == CALLBACK_TIMEOUT

    monkeypatch.setattr(services.urllib_request, "urlopen", mock_urlopen)

    services.update_pipeline_run_state(
        pipeline_run.uuid,
        {
            "state": RunStateEnum.RUNNING.name,
        },
    )
    assert len(pipeline_run.pipeline_run_states) == 3
    assert pipeline_run.run_state_enum() == RunStateEnum.RUNNING


@patch("app.pipelines.services.upload_stream")
@patch("app.pipelines.models.create_url")
@patch("app.pipelines.services.urllib_request.urlopen")
def test_copy_pipeline_run_artifact(
    urlopen_mock, create_url_mock, upload_stream_mock, pipeline
):
    create_url_mock.return_value = "http://example.com/presigned"
    urlopen_mock.return_value = io.BytesIO(b"this is data")
    another_run = services.create_pipeline_run(
        pipeline.uuid, VALID_CALLBACK_INPUT, True
    )
    pipeline_run = services.create_pipeline_run(
        pipeline.uuid, VALID_CALLBACK_INPUT, True
    )
    artifact = PipelineRunArtifact(name="ex.csv", pipeline_run=pipeline_run)
    db.session.add(artifact)
    db.session.commit()

    services.copy_pipeline_run_artifact(artifact, another_run)
    assert len(another_run.pipeline_run_inputs) == 1
    assert another_run.pipeline_run_inputs[0].filename == "ex.csv"
    assert another_run.pipeline_run_inputs[0].url == "http://example.com/presigned"


def test_create_pipeline_run_artifact_no_pipeline(app):
    with pytest.raises(ValueError):
        services.create_pipeline_run_artifact("nosuchid", "file.name", None)
