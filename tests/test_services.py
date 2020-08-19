import pytest
from app import services

A_NAME = 'a pipeline'
A_DESCRIPTION = 'a description'
A_DOCKER_IMAGE = 'example/image'
A_SSH_URL = 'git@github.com:an_org/a_repo.git'
A_BRANCH = 'master'
A_VERSION = '1.0'


def test_create_pipeline_version_no_urls(app):
    # Can't create a pipeline without some kind of URL configuration.
    with pytest.raises(ValueError):
        services.create_pipeline_version(
            A_NAME, A_DESCRIPTION, A_VERSION, '', '', '')


def test_create_pipeline_version(app):
    # Given: good fields
    pipeline_version = services.create_pipeline_version(
        A_NAME, A_DESCRIPTION, A_VERSION, A_DOCKER_IMAGE, A_SSH_URL, A_BRANCH)
    # Then: a pipeline is created
    assert pipeline_version.version == A_VERSION
    assert pipeline_version.pipeline.name == A_NAME
    assert pipeline_version.pipeline.description == A_DESCRIPTION
    assert pipeline_version.pipeline.docker_image_url == A_DOCKER_IMAGE
    assert pipeline_version.pipeline.repository_ssh_url == A_SSH_URL
    assert pipeline_version.pipeline.repository_branch == A_BRANCH
