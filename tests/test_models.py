from app.models import db, Pipeline


def test_create_pipeline(app):
    """ A new pipeline model does save to the database. """
    pipeline = Pipeline(name="a pipeline", description="a description",)
    db.session.add(pipeline)
    db.session.commit()

    assert set(Pipeline.query.all()) == set([pipeline])
    assert len(pipeline.uuid) > 0
