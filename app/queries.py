from .models import Pipeline
from sqlalchemy import and_


def find_pipeline(uuid):
    """ Find a pipelines """
    return Pipeline.query.filter(
        and_(Pipeline.uuid == uuid, Pipeline.is_deleted == False,)
    ).one_or_none()


def find_pipelines():
    """ Find all pipelines """
    return Pipeline.query.filter(Pipeline.is_deleted == False)
