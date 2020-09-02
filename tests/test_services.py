import pytest

from app import services
from app.models import db
from app.queries import find_pipeline

A_NAME = "a pipeline"
A_DESCRIPTION = "a description"
A_DOCKER_IMAGE = "example/image"
A_SSH_URL = "git@github.com:an_org/a_repo.git"
A_BRANCH = "master"


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


def test_create_pipeline_run_no_pipeline(app):
    with pytest.raises(ValueError):
        pipeline_run = services.create_pipeline_run("no-id", [])


def test_create_pipeline_run(app, pipeline):
    input1 = {
        "name": "name1.pdf",
        "url": "https://example.com/name1.pdf",
    }
    input2 = {
        "name": "name2.pdf",
        "url": "https://example.com/name2.pdf",
    }
    pipeline_run = services.create_pipeline_run(pipeline.uuid, [input1, input2])
    assert pipeline_run.pipeline == pipeline
    assert pipeline_run.sequence == 1
    assert len(pipeline_run.pipeline_run_inputs) == 2
    assert pipeline_run.pipeline_run_inputs[0].filename == input1["name"]
    assert pipeline_run.pipeline_run_inputs[1].filename == input2["name"]
    assert len(pipeline_run.pipeline_run_states) == 1


def test_update_pipeline_run_output(app, pipeline):
    with pytest.raises(ValueError):
        services.update_pipeline_run_output(None, "stdout", "stderr")

    pipeline_run = services.create_pipeline_run(pipeline.uuid, [])
    db.session.commit()

    services.update_pipeline_run_output(pipeline_run.uuid, "stdout", "stderr")
    assert pipeline_run.std_out == "stdout"
    assert pipeline_run.std_err == "stderr"
