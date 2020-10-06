import pytest
from app import create_app
from app.constants import (
    MAX_CONTENT_LENGTH,
    S3_ENDPOINT_URL,
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
)


@pytest.fixture
def app():
    # create a temporary file to isolate the database for each test
    (app, db, _) = create_app(
        {
            SQLALCHEMY_DATABASE_URI: "sqlite://",
            "TESTING": True,
            "DEBUG": True,
            SECRET_KEY: "PYTEST",
            MAX_CONTENT_LENGTH: "100",
            S3_ENDPOINT_URL: "http://example.com",
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
