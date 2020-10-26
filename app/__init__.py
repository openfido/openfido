import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from .auth import auth_bp
from .org import org_bp
from .models import db

from blob_utils import constants

# Allow a specific set of environmental variables to be configurable:
CONFIG_VARS = (
    "SECRET_KEY",
    "SQLALCHEMY_DATABASE_URI",
    constants.S3_ACCESS_KEY_ID,
    constants.S3_SECRET_ACCESS_KEY,
    constants.S3_ENDPOINT_URL,
    constants.S3_REGION_NAME,
    constants.S3_BUCKET,
    constants.S3_PRESIGNED_TIMEOUT,
)


def create_app(config=None):
    """ Create initial app. """
    app = Flask(__name__)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object("app.default_settings")

    environmental_vars = dict(
        (var, os.environ.get(var)) for var in os.environ.keys() if var in CONFIG_VARS
    )

    app.config.from_mapping(environmental_vars)

    if config is not None:
        app.config.from_mapping(config)

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(auth_bp, url_prefix="/users")
    app.register_blueprint(org_bp, url_prefix="/organizations")

    @app.route("/healthcheck")
    def healthcheck():
        return "OK"

    return (app, db, migrate)
