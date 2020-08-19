from .models import Pipeline, PipelineVersion, db


def create_pipeline_version(
        name, description, version, docker_image_url, repository_ssh_url, repository_branch
):
    """ Create a Pipeline.

    Note: The db.session is not committed. Be sure to commit the session.
    """
    pipeline = Pipeline(
        name=name,
        description=description,
        docker_image_url=docker_image_url,
        repository_ssh_url=repository_ssh_url,
        repository_branch=repository_branch,
    )
    pipeline_version = PipelineVersion(version=version)
    pipeline.versions.append(pipeline_version)
    db.session.add(pipeline)

    return pipeline_version
