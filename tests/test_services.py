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


def test_create_pipeline_version(app):
    # Given: good fields
    pipeline = services.create_pipeline(
        A_NAME, A_DESCRIPTION, A_DOCKER_IMAGE, A_SSH_URL, A_BRANCH
    )
    # Then: a pipeline is created
    assert pipeline.name == A_NAME
    assert pipeline.description == A_DESCRIPTION
    assert pipeline.docker_image_url == A_DOCKER_IMAGE
    assert pipeline.repository_ssh_url == A_SSH_URL
    assert pipeline.repository_branch == A_BRANCH


def test_delete_pipeline_no_record(app):
    with pytest.raises(ValueError):
        services.delete_pipeline("fake-id")


def test_delete_pipeline(app):
    pipeline = services.create_pipeline(
        A_NAME, A_DESCRIPTION, A_DOCKER_IMAGE, A_SSH_URL, A_BRANCH
    )
    db.session.add(pipeline)
    db.session.commit()

    services.delete_pipeline(pipeline.uuid)

    assert pipeline.is_deleted
