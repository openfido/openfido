import pytest

from app import create_app


@pytest.fixture
def app():
    # create a temporary file to isolate the database for each test
    (app, db, _, _) = create_app(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "TESTING": True,
            "DEBUG": True,
            "SECRET_KEY": "PYTEST",
            "CELERY_ALWAYS_EAGER": True,
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
