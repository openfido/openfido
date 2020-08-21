from .models import Pipeline, db
from .queries import find_pipeline


def delete_pipeline(uuid):
    """ Delete a pipeline.

    Note: The db.session is not committed. Be sure to commit the session.
    """
    pipeline = find_pipeline(uuid)
    if pipeline is None:
        raise ValueError("no pipeline found")

    pipeline.is_deleted = True


def create_pipeline(
    name, description, docker_image_url, repository_ssh_url, repository_branch
):
    """ Create a Pipeline.

    Note: The db.session is not committed. Be sure to commit the session.
    """
    if len(name) == 0 or len(description) == 0:
        raise ValueError("name and description must be supplied.")
    if len(docker_image_url) == 0:
        raise ValueError("A docker image URL must be supplied.")
    if len(repository_ssh_url) == 0 or len(repository_branch) == 0:
        raise ValueError("A ssh URL must be supplied.")

    pipeline = Pipeline(
        name=name,
        description=description,
        docker_image_url=docker_image_url,
        repository_ssh_url=repository_ssh_url,
        repository_branch=repository_branch,
    )
    db.session.add(pipeline)

    return pipeline
