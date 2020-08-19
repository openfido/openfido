from app.models import db, Pipeline, PipelineVersion


def test_create_pipeline(app):
    """ A new pipeline model does save to the database. """
    pipeline = Pipeline(name="a pipeline", description="a description",)
    db.session.add(pipeline)
    db.session.commit()

    assert set(Pipeline.query.all()) == set([pipeline])


def test_create_pipeline_version(app):
    """ A new pipeline_version model does save to the database. """
    pipeline = Pipeline(name="a pipeline", description="a description",)
    pipeline_version = PipelineVersion(version="1.0.1")
    pipeline.versions.append(pipeline_version)
    db.session.add(pipeline)
    db.session.commit()

    assert set(PipelineVersion.query.all()) == set([pipeline_version])
