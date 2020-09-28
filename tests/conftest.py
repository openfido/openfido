import pytest
from app import create_app
from app.constants import (
    CELERY_ALWAYS_EAGER,
    MAX_CONTENT_LENGTH,
    S3_ENDPOINT_URL,
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    WORKER_API_SERVER,
    WORKER_API_TOKEN,
)
from app.model_utils import SystemPermissionEnum
from app.pipelines.models import Pipeline, db
from app.pipelines.services import execute_pipeline
from app.workflows.models import Workflow, WorkflowPipeline, WorkflowPipelineDependency
from app.workflows.services import create_workflow_pipeline
from roles.services import create_application


@pytest.fixture
def app():
    # create a temporary file to isolate the database for each test
    (app, db, _, _) = create_app(
        {
            SQLALCHEMY_DATABASE_URI: "sqlite://",
            "TESTING": True,
            "DEBUG": True,
            SECRET_KEY: "PYTEST",
            CELERY_ALWAYS_EAGER: True,
            MAX_CONTENT_LENGTH: "100",
            S3_ENDPOINT_URL: "http://example.com",
            WORKER_API_SERVER: "http://example.com",
            WORKER_API_TOKEN: "atoken",
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
    pipeline = Pipeline(
        name="a pipeline",
        description="a description",
        docker_image_url="",
        repository_ssh_url="",
        repository_branch="",
    )
    db.session.add(pipeline)
    db.session.commit()

    return pipeline


@pytest.fixture
def workflow(app):
    workflow = Workflow(
        name="a workflow",
        description="a description",
    )
    db.session.add(workflow)
    db.session.commit()

    return workflow


@pytest.fixture
def workflow_pipeline(app, workflow, pipeline):
    workflow_pipeline = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    db.session.add(workflow_pipeline)
    db.session.commit()

    return workflow_pipeline


@pytest.fixture
def mock_execute_pipeline(app, pipeline, monkeypatch):
    def no_op(*args, **kwargs):
        pass

    monkeypatch.setattr(execute_pipeline, "delay", no_op)

    return no_op


@pytest.fixture
def client_application(app):
    return create_application("test client", SystemPermissionEnum.PIPELINES_CLIENT)


@pytest.fixture
def worker_application(app):
    return create_application("test client", SystemPermissionEnum.PIPELINES_WORKER)


@pytest.fixture
def workflow_line(app, pipeline, workflow):
    """ Three pipelines that feed into one another """
    pipeline_a = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    pipeline_b = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    pipeline_c = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    db.session.add(pipeline_a)
    db.session.add(pipeline_b)
    db.session.add(pipeline_c)
    db.session.commit()

    a_to_b = WorkflowPipelineDependency(
        from_workflow_pipeline=pipeline_a,
        to_workflow_pipeline=pipeline_b,
    )
    b_to_c = WorkflowPipelineDependency(
        from_workflow_pipeline=pipeline_b,
        to_workflow_pipeline=pipeline_c,
    )
    db.session.add(a_to_b)
    db.session.add(b_to_c)
    db.session.commit()

    return workflow


@pytest.fixture
def workflow_square(app, pipeline, workflow):
    """ Four pipelines forming a diamond """
    pipeline_a = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    pipeline_b = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    pipeline_c = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    pipeline_d = WorkflowPipeline(workflow=workflow, pipeline=pipeline)
    db.session.add(pipeline_a)
    db.session.add(pipeline_b)
    db.session.add(pipeline_c)
    db.session.add(pipeline_d)
    db.session.commit()

    a_to_b = WorkflowPipelineDependency(
        from_workflow_pipeline=pipeline_a,
        to_workflow_pipeline=pipeline_b,
    )
    a_to_c = WorkflowPipelineDependency(
        from_workflow_pipeline=pipeline_a,
        to_workflow_pipeline=pipeline_c,
    )
    b_to_d = WorkflowPipelineDependency(
        from_workflow_pipeline=pipeline_b,
        to_workflow_pipeline=pipeline_d,
    )
    c_to_d = WorkflowPipelineDependency(
        from_workflow_pipeline=pipeline_c,
        to_workflow_pipeline=pipeline_d,
    )
    db.session.add(a_to_b)
    db.session.add(a_to_c)
    db.session.add(b_to_d)
    db.session.add(c_to_d)
    db.session.commit()

    return workflow
