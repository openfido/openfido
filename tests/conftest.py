import pytest

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
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()
