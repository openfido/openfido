from app import worker


def test_celery():
    assert worker.celery is not None
