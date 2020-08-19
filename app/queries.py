from .models import Pipeline


def find_pipelines():
    """ Find all pipelines """
    return Pipeline.query
