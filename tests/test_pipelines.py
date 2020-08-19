from app.models import db, Pipeline


# TODO at least one of the url params must be non-empty

def test_create_pipeline(client):
    params = {
        'name': 'a pipeline',
        'description': 'a description',
        'version': 'version',
        'docker_image_url': 'a/url',
        'repository_ssh_url': 'ssh+github url',
        'repository_branch': 'master',
    }
    result = client.post(
        "/v1/pipelines",
        content_type="application/json",
        json=params,
    )
    assert result.status_code == 200

    pipeline = Pipeline.query.filter(Pipeline.name == params['name']).one_or_none()
    assert pipeline.name == 'a pipeline'
    assert len(pipeline.versions) == 1
    assert pipeline.versions[0].version == 'version'

    # TODO when jobs are like...real, we would then assert that the job is
    # started or rather that some celery method has been called (delay)
