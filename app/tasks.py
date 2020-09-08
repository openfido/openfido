import json
import os
import urllib.request

from celery import Celery, Task, shared_task
from celery.utils.log import get_task_logger

from app.constants import WORKER_API_TOKEN
from app.models import RunStateEnum
from roles.decorators import ROLES_KEY

# make the request lib mockable for testing:
urllib_request = urllib.request

logger = get_task_logger(__name__)


def make_celery(app):
    """ Create a celery client. """
    celery = Celery(app.import_name)
    celery.conf.update(app.config)

    class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery


def update_run_status(uuid, run_uuid, run_state_enum):
    url = f"{os.environ['WORKER_API_SERVER']}/v1/pipelines/{uuid}/runs/{run_uuid}/state"
    headers = {
        ROLES_KEY: os.environ[WORKER_API_TOKEN],
        "content-type": "application/json",
    }
    data = json.dumps({"state": run_state_enum.name})

    request = urllib_request.Request(url, data.encode("ascii"), headers, method="PUT")
    try:
        urllib_request.urlopen(request)
        # TODO verify response.
    except URLError as e:
        logger.warning(e)


@shared_task
def execute_pipeline(
    pipeline_uuid,
    pipeline_run_uuid,
    docker_image_url,
    repository_ssh_url,
    repository_branch,
):
    # TODO if we can't even mark it as running, tell celery to put the job back
    # on the queue?
    update_run_status(pipeline_uuid, pipeline_run_uuid, RunStateEnum.RUNNING)
    logger.info("executed")
    update_run_status(pipeline_uuid, pipeline_run_uuid, RunStateEnum.COMPLETED)
    # TODO need params for the WORKER SERVER and an API_KEY
    # TODO Make a call to the application updating the status to FINISHED.
