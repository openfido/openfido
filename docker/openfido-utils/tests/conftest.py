import pytest
import requests

from flask import Flask
from flask_migrate import Migrate
from application_roles.models import db


@pytest.fixture
def app():
    app = Flask(__name__)

    app.config.from_mapping(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "TESTING": True,
            "DEBUG": True,
            "SECRET_KEY": "PYTEST",
        }
    )

    db.init_app(app)

    Migrate(app, db)

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def session():
    session = requests.Session()
    session.headers["Workflow-API-Key"] = "workflow-api-key"
    session.headers["X-Organization"] = "organization-1"

    return session
