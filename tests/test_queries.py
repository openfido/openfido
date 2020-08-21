from app.models import Pipeline, db
from app.queries import find_pipeline, find_pipelines


def test_find_pipeline_no_uuid(app):
    assert find_pipeline("no-id") is None


def test_find_pipeline_is_deleted(app):
    pipeline = Pipeline(name="a pipeline", description="a description", is_deleted=True)
    db.session.add(pipeline)
    db.session.commit()

    assert find_pipeline(pipeline.uuid) is None


def test_find_pipeline(app):
    pipeline = Pipeline(name="a pipeline", description="a description",)
    db.session.add(pipeline)
    db.session.commit()

    assert find_pipeline(pipeline.uuid) == pipeline


def test_find_pipelines_no_pipelines(app):
    assert list(find_pipelines()) == []


def test_find_pipelines(app):
    p1 = Pipeline(name="a pipeline", description="a description",)
    p2 = Pipeline(name="a pipeline", description="a description", is_deleted=True)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()

    assert set(find_pipelines()) == set([p1])
