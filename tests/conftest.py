import pytest
from app import create_app
from app.constants import (
    MAX_CONTENT_LENGTH,
    S3_ENDPOINT_URL,
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    AUTH_HOSTNAME,
    WORKFLOW_HOSTNAME,
    WORKFLOW_API_TOKEN,
)
from app.pipelines.models import db, OrganizationPipeline

ORGANIZATION_UUID = "4d96f0b6fe9a4872813b3fac7a675505"
PIPELINE_UUID = "0" * 32
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


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def pipeline(app):
    op = OrganizationPipeline(organization_uuid=ORGANIZATION_UUID, pipeline_uuid=PIPELINE_UUID)
    db.session.add(op)
    db.session.commit()

    return op
