import json
import os
import subprocess
import tempfile
import urllib

from celery import Celery, Task, shared_task
from celery.utils.log import get_task_logger
from flask import current_app

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


class RunExecutor:
    """ An Pipeline API caller within the context of a specific pipeline run. """

    def __init__(self, uuid, run_uuid):
        self.uuid = uuid
        self.run_uuid = run_uuid
        self.stdout = ""
        self.stderr = ""

    def _make_request(self, path, data):
        server = current_app.config["WORKER_API_SERVER"]
        url = f"{server}/v1/pipelines/{self.uuid}/runs/{self.run_uuid}/{path}"
        headers = {
            ROLES_KEY: current_app.config[WORKER_API_TOKEN],
            "content-type": "application/json",
        }

        request = urllib_request.Request(
            url, json.dumps(data).encode("ascii"), headers, method="PUT"
        )
        urllib_request.urlopen(request)

    def update_run_output(self, stdout, stderr=""):
        """ Append addition stdout/stderr to run's output. """
        self.stdout += "\n" + stdout
        self.stderr += "\n" + stderr
        data = {"std_out": self.stdout, "std_err": self.stderr}
        return self._make_request("console", data)

    def update_run_status(self, run_state_enum):
        return self._make_request("state", {"state": run_state_enum.name})

    def run(self, command, directory):
        """ Execute a command, raise an exception on nonzero error codes. """
        self.update_run_output(f"Run: {command}")
        result = subprocess.run(command.split(" "), cwd=directory, capture_output=True)

        logger.debug(result)

        self.update_run_output(
            result.stdout.decode("utf-8"), result.stderr.decode("utf-8")
        )

        if result.returncode != 0:
            raise ValueError(f"Command returned nonzero code: {result.returncode}")


@shared_task
def execute_pipeline(
    pipeline_uuid,
    pipeline_run_uuid,
    input_files,
    docker_image_url,
    repository_ssh_url,
    repository_branch,
):
    def failed(err):
        try:
            executor.update_run_output("", str(err))
            executor.update_run_status(RunStateEnum.FAILED)
        except urllib.error.URLError as url_e:
            logger.error(url_e)

    try:
        executor = RunExecutor(pipeline_uuid, pipeline_run_uuid)
        executor.update_run_status(RunStateEnum.RUNNING)

        with tempfile.TemporaryDirectory() as tmpdirname:
            gitdirname = f"{tmpdirname}/gitrepo"

            executor.run(f"docker pull {docker_image_url}", tmpdirname)
            executor.run(f"git clone {repository_ssh_url} gitrepo", tmpdirname)
            executor.run(f"git checkout {repository_branch}", gitdirname)

            if not os.path.exists(f"{tmpdirname}/gitrepo/openfido.sh"):
                raise ValueError("Openfido.sh does not exist in repository")

            executor.run("mkdir input", gitdirname)
            executor.run("mkdir output", gitdirname)

            for input_file in input_files:
                urllib_request.urlretrieve(
                    input_file["url"], f"{gitdirname}/input/{input_file['name']}"
                )

            # input/output should not  be in the github repo
            executor.run(
                (
                    "docker run --rm "
                    f"-v {gitdirname}:/tmp/gitrepo "
                    f"-v {tmpdirname}/input:/tmp/input "
                    f"-v {tmpdirname}/output:/tmp/output "
                    "-w /tmp/gitrepo "
                    f"{docker_image_url} sh openfido.sh /tmp/input /tmp/output"
                ),
                gitdirname,
            )

            # TODO upload any artifacts that were found.
        executor.update_run_status(RunStateEnum.COMPLETED)
    except ValueError as v_e:
        failed(v_e)
    except urllib.error.URLError as url_e:
        failed(url_e)
