import os

from flask import Flask
from flask_migrate import Migrate

from application_roles.model_utils import get_db

from .pipelines import models as pipeline_models
from . import constants

db = get_db()

# Allow a specific set of environmental variables to be configurable:
CONFIG_VARS = (
    constants.SECRET_KEY,
    constants.SQLALCHEMY_DATABASE_URI,
    constants.S3_ACCESS_KEY_ID,
    constants.S3_SECRET_ACCESS_KEY,
    constants.S3_ENDPOINT_URL,
    constants.S3_REGION_NAME,
    constants.S3_BUCKET,
)


def create_app(config=None):
    """ Create initial app. """
    app = Flask(__name__)
    app.config.from_object("app.default_settings")

    environmental_vars = dict(
        (var, os.environ.get(var)) for var in os.environ if var in CONFIG_VARS
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

    # app.register_blueprint(pipeline_bp, url_prefix="/v1/organizations")

    return (app, db, migrate)
