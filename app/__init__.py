import os

from flask import Flask
from flask_migrate import Migrate

# not used, just want it included in our app's schema
from roles.models import db as roles_db

from .models import db
from .pipelines import pipeline_bp
from .tasks import make_celery

# Allow a specific set of environmental variables to be configurable:
CONFIG_VARS = (
    "SECRET_KEY",
    "SQLALCHEMY_DATABASE_URI",
    "CELERY_RESULT_BACKEND",
    "CELERY_BROKER_URL",
    "CELERY_ALWAYS_EAGER",
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

    app.register_blueprint(pipeline_bp, url_prefix="/v1/pipelines")

    return (app, db, celery, migrate)
