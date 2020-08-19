from .models import Pipeline


def find_pipeline(uuid):
    """ Find a pipelines """
    return Pipeline.query.filter(Pipeline.uuid == uuid).one_or_none()


def find_pipelines():
    """ Find all pipelines """
    return Pipeline.query
