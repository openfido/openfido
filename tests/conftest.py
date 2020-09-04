import pytest

from app import create_app
from app.constants import (
    CELERY_ALWAYS_EAGER,
    MAX_CONTENT_LENGTH,
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
)
from app.models import Pipeline, SystemPermissionEnum, db
from roles.services import create_application


@pytest.fixture
def app():
    # create a temporary file to isolate the database for each test
    (app, db, _, _) = create_app(
        {
            SQLALCHEMY_DATABASE_URI: "sqlite://",
            "TESTING": True,
            "DEBUG": True,
            SECRET_KEY: "PYTEST",
            CELERY_ALWAYS_EAGER: True,
            MAX_CONTENT_LENGTH: "100",
        }
    )

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def pipeline(app):
    pipeline = Pipeline(
        name="a pipeline",
        description="a description",
        docker_image_url="",
        repository_ssh_url="",
        repository_branch="",
    )
    db.session.add(pipeline)
    db.session.commit()

    return pipeline


@pytest.fixture
def client_application(app):
    return create_application("test client", SystemPermissionEnum.PIPELINES_CLIENT)


@pytest.fixture
def worker_application(app):
    return create_application("test client", SystemPermissionEnum.PIPELINES_WORKER)
