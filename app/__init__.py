import os

from flask import Flask
from flask_migrate import Migrate

# not used, just want it included in our app's schema
from roles.models import db as roles_db

from . import constants
from .models import db
from .routes import pipeline_bp, run_bp
from .tasks import make_celery

# Allow a specific set of environmental variables to be configurable:
CONFIG_VARS = (
    constants.SECRET_KEY,
    constants.SQLALCHEMY_DATABASE_URI,
    constants.CELERY_RESULT_BACKEND,
    constants.CELERY_BROKER_URL,
    constants.CELERY_ALWAYS_EAGER,
    constants.BLOB_API_SERVER,
    constants.BLOB_API_TOKEN,
    constants.MAX_CONTENT_LENGTH,
    constants.WORKER_API_SERVER,
    constants.WORKER_API_TOKEN,
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

    if app.config[constants.MAX_CONTENT_LENGTH] is not None:
        app.config[constants.MAX_CONTENT_LENGTH] = int(
            app.config[constants.MAX_CONTENT_LENGTH]
        )

    db.init_app(app)
    migrate = Migrate(app, db)

    celery = make_celery(app)

    app.register_blueprint(pipeline_bp, url_prefix="/v1/pipelines")
    app.register_blueprint(run_bp, url_prefix="/v1/pipelines")

    return (app, db, celery, migrate)
