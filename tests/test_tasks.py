from app.services import create_pipeline_run
from app.tasks import make_celery, execute_pipeline, urllib_request

from .test_services import VALID_CALLBACK_INPUT


def test_make_celery(app):
    celery = make_celery(app)

    @celery.task()
    def add_numbers(a, b):
        return a + b

    assert add_numbers.delay(10, 12).wait() == 22


def test_execute_pipeline(app, pipeline, monkeypatch):
    pipeline_run = create_pipeline_run(pipeline.uuid, VALID_CALLBACK_INPUT)

    def no_op(*args, **kwargs):
        pass

    monkeypatch.setattr(urllib_request, "urlopen", no_op)

    execute_pipeline(
        pipeline.uuid,
        pipeline_run.uuid,
        "",
        "",
        "",
    )
