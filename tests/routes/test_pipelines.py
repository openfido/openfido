from app.models import Pipeline, db
from app.queries import find_pipeline
from roles.decorators import ROLES_KEY


def test_create_pipeline_wrong_content_type(client):
    result = client.post(
        "/v1/pipelines",
        content_type="application/badtype",
    )
    assert result.status_code == 400


def test_create_pipeline_no_params(client):
    # An error is returned if no configuration information is supplied.
    result = client.post("/v1/pipelines", content_type="application/json", json={})
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
    result = client.post(
        "/v1/pipelines",
        content_type="application/json",
        json=params,
    )
    assert result.status_code == 400


def test_create_pipeline_non_empty_params(client, client_application):
    db.session.commit()
    # An error is returned if no configuration information is supplied.
    params = {
        "name": "a pipeline",
        "description": "a description",
        "docker_image_url": "",
        "repository_ssh_url": "",
        "repository_branch": "",
    }
    result = client.post(
        "/v1/pipelines",
        content_type="application/json",
        json=params,
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400


def test_create_pipeline_no_auth(client):
    params = {
        "name": "a pipeline",
        "description": "a description",
        "docker_image_url": "a/url",
        "repository_ssh_url": "ssh+github url",
        "repository_branch": "master",
    }
    result = client.post(
        "/v1/pipelines",
        content_type="application/json",
        json=params,
    )
    assert result.status_code == 401


def test_create_pipeline_wrong_auth(client, worker_application):
    db.session.commit()
    # using an api_key that doesn't have client permissions will fail:
    params = {
        "name": "a pipeline",
        "description": "a description",
        "docker_image_url": "a/url",
        "repository_ssh_url": "ssh+github url",
        "repository_branch": "master",
    }
    result = client.post(
        "/v1/pipelines",
        content_type="application/json",
        json=params,
        headers={ROLES_KEY: worker_application.api_key},
    )
    assert result.status_code == 401


def test_create_pipeline(client, client_application):
    db.session.commit()
    params = {
        "name": "a pipeline",
        "description": "a description",
        "docker_image_url": "a/url",
        "repository_ssh_url": "ssh+github url",
        "repository_branch": "master",
    }
    result = client.post(
        "/v1/pipelines",
        content_type="application/json",
        json=params,
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200

    pipeline = Pipeline.query.filter(Pipeline.name == params["name"]).one_or_none()
    assert pipeline.name == "a pipeline"


def test_list_pipelines(client, client_application):
    db.session.commit()
    result = client.get(
        "/v1/pipelines",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert len(result.json) == 0

    p1 = Pipeline(
        name="pipeline 1",
        description="a description",
        docker_image_url="",
        repository_ssh_url="",
        repository_branch="",
    )
    db.session.add(p1)
    p2 = Pipeline(
        name="pipeline 2",
        description="a description",
        docker_image_url="",
        repository_ssh_url="",
        repository_branch="",
    )
    db.session.add(p2)
    db.session.commit()

    result = client.get(
        "/v1/pipelines",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert len(result.json) == 2
    assert result.json[0]["name"] == p1.name
    assert result.json[1]["name"] == p2.name


def test_get_pipeline_no_match(client, client_application):
    db.session.commit()
    result = client.get(
        "/v1/pipelines/1111ddddeeee2222",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 404


def test_get_pipeline(client, pipeline, client_application):
    db.session.commit()
    result = client.get(
        f"/v1/pipelines/{pipeline.uuid}",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200


def test_remove_pipeline_no_match(client, client_application):
    db.session.commit()
    result = client.delete(
        "/v1/pipelines/1111ddddeeee2222",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400


def test_remove_pipeline(client, pipeline, client_application):
    db.session.commit()
    result = client.delete(
        f"/v1/pipelines/{pipeline.uuid}",
        content_type="application/json",
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert find_pipeline(pipeline.uuid) is None


def test_update_pipeline_bad_id(client, client_application):
    db.session.commit()
    params = {
        "name": "updated pipeline",
        "description": "updated description",
        "docker_image_url": "updated url",
        "repository_ssh_url": "updated ssh",
        "repository_branch": "updated branch",
    }
    result = client.put(
        f"/v1/pipelines/noid",
        content_type="application/json",
        json=params,
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 400


def test_update_pipeline(client, client_application, pipeline):
    db.session.commit()
    params = {
        "name": "updated pipeline",
        "description": "updated description",
        "docker_image_url": "updated url",
        "repository_ssh_url": "updated ssh",
        "repository_branch": "updated branch",
    }
    result = client.put(
        f"/v1/pipelines/{pipeline.uuid}",
        content_type="application/json",
        json=params,
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200

    pipeline = Pipeline.query.filter(Pipeline.name == params["name"]).one_or_none()
    assert pipeline.name == "updated pipeline"
    assert pipeline.description == "updated description"
    assert pipeline.docker_image_url == "updated url"
    assert pipeline.repository_ssh_url == "updated ssh"
    assert pipeline.repository_branch == "updated branch"


def test_search_pipelines(client, client_application, pipeline):
    db.session.commit()
    result = client.post(
        "/v1/pipelines/search",
        content_type="application/json",
        json={"search": "pipe"},
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert len(result.json) == 1

    result = client.post(
        "/v1/pipelines/search",
        content_type="application/json",
        json={"search": "nomatch"},
        headers={ROLES_KEY: client_application.api_key},
    )
    assert result.status_code == 200
    assert len(result.json) == 0
