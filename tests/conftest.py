import uuid
from datetime import datetime, timedelta
import pytest
import responses
from app import create_app
from app.constants import (
    AUTH_HOSTNAME,
    MAX_CONTENT_LENGTH,
    S3_ENDPOINT_URL,
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    WORKFLOW_API_TOKEN,
    WORKFLOW_HOSTNAME,
)
from app.pipelines.models import (
    OrganizationPipeline,
    OrganizationPipelineRun,
    OrganizationPipelineInputFile,
    db,
)
from app.utils import ApplicationsEnum
from application_roles.services import create_application

ORGANIZATION_UUID = "4d96f0b6fe9a4872813b3fac7a675505"
PIPELINE_UUID = "0" * 32
PIPELINE_RUN_UUID = "d6c42c749a1643aba0217c02e177625f"
PIPELINE_RUN_INPUT_FILE_UUID = "1a393d3d847d41b4bbf006738bb576c5"
USER_UUID = "ded3f053-d25e-4873-8e38-7fbf9c38"
JWT_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dWlkIjoiZGVkM2YwNTMtZDI1ZS00ODczLThlMzgtN2ZiZjljMzgiLCJleHAiOjE2MDMyOTQ3MzYsIm1heC1leHAiOjE2MDU3MTM5MzYsImlzcyI6ImFwcCIsImlhdCI6MTYwMjA4NTEzNn0.YRVky4oynBJRF6XhchCvDzeEqUOxAaki-xPTnXmAd3Y"


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
            AUTH_HOSTNAME: "http://auth",
            WORKFLOW_HOSTNAME: "http://workflow",
            WORKFLOW_API_TOKEN: "workflow-api-token",
        }
    )

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def organization_pipeline(app):
    op = OrganizationPipeline(
        organization_uuid=ORGANIZATION_UUID, pipeline_uuid=PIPELINE_UUID
    )
    db.session.add(op)
    db.session.commit()

    return op


@pytest.fixture
def organization_pipeline_input_file(app, organization_pipeline):
    opif = OrganizationPipelineInputFile(
        uuid=PIPELINE_RUN_INPUT_FILE_UUID,
        organization_pipeline_id=organization_pipeline.id,
        name=f"{PIPELINE_UUID}organization_pipeline_input_file.csv",
    )
    db.session.add(opif)
    db.session.commit()

    return opif


@pytest.fixture
def organization_pipeline_run(app, organization_pipeline):
    opr = OrganizationPipelineRun(
        uuid=PIPELINE_RUN_UUID,
        organization_pipeline_id=organization_pipeline.id,
        pipeline_run_uuid=PIPELINE_RUN_UUID,
        status_update_token=uuid.uuid4().hex,
        status_update_token_expires_at=datetime.now() + timedelta(days=7),
        share_token=uuid.uuid4().hex,
        share_password_hash=None,
        share_password_salt=None,
    )
    db.session.add(opr)
    db.session.commit()

    return opr


@pytest.fixture
def client_application(app):
    application = create_application("test client", ApplicationsEnum.REACT_CLIENT)

    db.session.add(application)
    db.session.commit()

    responses.add(
        responses.GET,
        f"{app.config[AUTH_HOSTNAME]}/users/{USER_UUID}/organizations",
        json=[
            {
                "created_at": "Wed, 07 Oct 2020 19:50:00 GMT",
                "name": "A test org",
                "updated_at": "Wed, 07 Oct 2020 19:50:00 GMT",
                "uuid": ORGANIZATION_UUID,
            }
        ],
    )

    return application
