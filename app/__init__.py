import os

from flask import Flask
from flask_migrate import Migrate
from .tasks import make_celery

from .models import db

# Allow a specific set of environmental variables to be configurable:
CONFIG_VARS = (
    "SECRET_KEY",
    "SQLALCHEMY_DATABASE_URI",
    "CELERY_RESULT_BACKEND",
    "CELERY_BROKER_URL",
)


def create_app(config=None):
    """ Create initial app. """
    app = Flask(__name__)
    app.config.from_object("app.default_settings")

    environmental_vars = dict(
        (var, os.environ.get(var)) for var in os.environ.keys() if var in CONFIG_VARS
    )

    app.config.from_mapping(environmental_vars)

    if config is not None:
        app.config.from_mapping(config)

    db.init_app(app)
    migrate = Migrate(app, db)

    celery = make_celery(app)

    @celery.task()
    def add_numbers(a, b):
        return a + b

    @app.route("/example")
    def example():
        result = add_numbers.delay(10, 12)
        result.wait()
        return f"Example: {result.result}"

    return (app, db, celery, migrate)
