from app.tasks import make_celery


def test_make_celery(app):
    celery = make_celery(app)
    celery.conf.task_always_eager = True

    @celery.task()
    def add_numbers(a, b):
        return a + b

    assert add_numbers.delay(10, 12).wait() == 22
