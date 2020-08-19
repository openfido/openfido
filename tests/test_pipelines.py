from app.models import db, Pipeline


def test_create_pipeline_wrong_content_type(client):
    result = client.post("/v1/pipelines", content_type="application/badtype",)
    assert result.status_code == 400


def test_create_pipeline_no_params(client):
    # An error is returned if no configuration information is supplied.
    params = {}
    result = client.post("/v1/pipelines", content_type="application/json", json=params,)
    assert result.status_code == 400


def test_create_pipeline_wrong_params(client):
    # An error is returned if no configuration information is supplied.
    params = {
        "wrong": "wrong",
        "name": "a pipeline",
        "description": "a description",
        "docker_image_url": "",
        "repository_ssh_url": "",
        "repository_branch": "",
    }
    result = client.post("/v1/pipelines", content_type="application/json", json=params,)
    assert result.status_code == 400


def test_create_pipeline_non_empty_params(client):
    # An error is returned if no configuration information is supplied.
    params = {
        "name": "a pipeline",
        "description": "a description",
        "docker_image_url": "",
        "repository_ssh_url": "",
        "repository_branch": "",
    }
    result = client.post("/v1/pipelines", content_type="application/json", json=params,)
    assert result.status_code == 400


def test_create_pipeline(client):
    params = {
        "name": "a pipeline",
        "description": "a description",
        "docker_image_url": "a/url",
        "repository_ssh_url": "ssh+github url",
        "repository_branch": "master",
    }
    result = client.post("/v1/pipelines", content_type="application/json", json=params,)
    assert result.status_code == 200

    pipeline = Pipeline.query.filter(Pipeline.name == params["name"]).one_or_none()
    assert pipeline.name == "a pipeline"
