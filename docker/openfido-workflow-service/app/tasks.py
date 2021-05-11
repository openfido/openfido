import json
import os
import subprocess
import tempfile
import urllib
from os.path import join
from urllib.parse import quote

from celery import Celery, Task, shared_task
from celery.utils.log import get_task_logger
from flask import current_app

from app.constants import WORKER_API_TOKEN
from app.model_utils import RunStateEnum
from application_roles.decorators import ROLES_KEY

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

    def _make_request(self, path, data, additional_headers, method="PUT"):
        server = current_app.config["WORKER_API_SERVER"]
        url = f"{server}/v1/pipelines/{self.uuid}/runs/{self.run_uuid}/{path}"
        headers = {
            ROLES_KEY: current_app.config[WORKER_API_TOKEN],
        }
        headers.update(additional_headers)

        request = urllib_request.Request(url, data, headers, method=method)
        urllib_request.urlopen(request)

    def _put(self, path, data):
        self._make_request(
            path,
            json.dumps(data).encode("ascii"),
            {
                "content-type": "application/json",
            },
        )

    def update_run_output(self, stdout, stderr=""):
        """ Append addition stdout/stderr to run's output. """
        if len(stdout) == 0 and len(stderr) == 0:
            # don't make an HTTP request that does nothing (many successful
            # commands actually don't produce any output at all)
            return

        self.stdout += "\n" + stdout
        self.stderr += "\n" + stderr
        data = {"std_out": self.stdout, "std_err": self.stderr}
        return self._put("console", data)

    def update_run_status(self, run_state_enum):
        return self._put("state", {"state": run_state_enum.name})

    def upload_artifact(self, filename, location):
        with open(location, "rb") as f:
            self._make_request(f"artifacts?name={quote(filename)}", f, {}, "POST")

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


@shared_task(ignore_result=True)
def execute_pipeline(
    pipeline_uuid,
    pipeline_run_uuid,
    input_files,
    docker_image_url,
    repository_ssh_url,
    repository_branch,
    repository_script,
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

        with tempfile.TemporaryDirectory() as tmpdir:
            gitdir = join(tmpdir, "gitrepo")
            inputdir = join(tmpdir, "input")
            outputdir = join(tmpdir, "output")

            executor.run(f"docker pull {docker_image_url}", tmpdir)
            executor.run(f"git clone --depth 1 {repository_ssh_url} gitrepo", tmpdir)
            executor.run(f"git checkout {repository_branch}", gitdir)

            if not os.path.exists(join(gitdir, repository_script)):
                raise ValueError("Repository script does not exist in repository")

            executor.run("mkdir input", tmpdir)
            executor.run("mkdir output", tmpdir)

            for input_file in input_files:
                urllib_request.urlretrieve(
                    input_file["url"], join(inputdir, input_file["name"])
                )

            executor.run("chmod -R 777 .", tmpdir)

            # TODO because these processes can take a long long time to run it'd
            # be ideal to poll the output every interval to give viewers a sense
            # of whether the job is doing.
            executor.run(
                (
                    "docker run --rm "
                    f"-v {gitdir}:/tmp/gitrepo "
                    f"-v {inputdir}:/tmp/input "
                    f"-v {outputdir}:/tmp/output "
                    f"-e OPENFIDO_INPUT=/tmp/input "
                    f"-e OPENFIDO_OUTPUT=/tmp/output "
                    "-w /tmp/gitrepo "
                    f"{docker_image_url} sh {repository_script}"
                ),
                gitdir,
            )

            for f in os.listdir(outputdir):
                if not os.path.isfile(join(outputdir, f)):
                    next
                executor.upload_artifact(f, join(outputdir, f))

        executor.update_run_status(RunStateEnum.COMPLETED)
    except Exception as exc:
        failed(exc)
