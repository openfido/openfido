import pytest

from unittest.mock import call, patch

from app.models import RunStateEnum
from app.services import create_pipeline_run
from app.tasks import execute_command, execute_pipeline, make_celery, update_run_status
from roles.decorators import ROLES_KEY

from .test_services import VALID_CALLBACK_INPUT


def test_make_celery(app):
    celery = make_celery(app)

    @celery.task()
    def add_numbers(a, b):
        return a + b

    assert add_numbers.delay(10, 12).wait() == 22


@patch("app.tasks.urllib_request.urlopen")
def test_update_run_status(urlopen_mock, app):
    update_run_status("uuid", "run_uuid", RunStateEnum.RUNNING)
    assert urlopen_mock.call_count == 1
    request = urlopen_mock.call_args_list[0][0][0]
    assert (
        request.full_url == "http://example.com/v1/pipelines/uuid/runs/run_uuid/state"
    )
    uppered_key = ROLES_KEY[0] + ROLES_KEY[1:].lower()
    assert uppered_key in request.headers.keys()
    assert RunStateEnum.RUNNING.name in request.data.decode("utf-8")


class ReturnValue:
    def __init__(self, value):
        self.returncode = value


@patch("app.tasks.subprocess.run")
def test_execute_command_failure(run_mock, app):
    run_mock.return_value = ReturnValue(1)

    with pytest.raises(ValueError):
        execute_command("a command", "/a/dir")

    run_mock.assert_called_once_with(
        ["a", "command"], cwd="/a/dir", capture_output=True
    )


@patch("app.tasks.subprocess.run")
def test_execute_command(run_mock, app):
    run_mock.return_value = ReturnValue(0)

    execute_command("a command", "/a/dir")
    run_mock.assert_called_once_with(
        ["a", "command"], cwd="/a/dir", capture_output=True
    )


@patch("app.tasks.update_run_status")
@patch("app.tasks.execute_command")
@patch("os.path.exists")
def test_execute_pipeline_no_openfido(
    exists_mock, execute_command_mock, update_run_status_mock, app
):
    exists_mock.return_value = False
    execute_command_mock.reset_mock()

    execute_pipeline(
        "uuid",
        "run_uuid",
        [],
        "python:3",
        "https://github.com/example",
        "master",
    )

    assert execute_command_mock.call_count == 3
    assert execute_command_mock.call_args_list[0][0][0] == "docker pull python:3"
    assert (
        execute_command_mock.call_args_list[1][0][0]
        == "git clone https://github.com/example gitrepo"
    )
    assert execute_command_mock.call_args_list[2][0][0] == "git checkout master"

    assert update_run_status_mock.call_count == 2
    assert update_run_status_mock.call_args_list[0] == call(
        "uuid", "run_uuid", RunStateEnum.RUNNING
    )
    assert update_run_status_mock.call_args_list[1] == call(
        "uuid", "run_uuid", RunStateEnum.FAILED
    )


@patch("app.tasks.update_run_status")
@patch("app.tasks.execute_command")
@patch("os.path.exists")
@patch("app.tasks.urllib_request.urlretrieve")
def test_execute_pipeline(
    urlretrieve_mock, exists_mock, execute_command_mock, update_run_status_mock, app
):
    exists_mock.return_value = True
    execute_command_mock.reset_mock()

    execute_pipeline(
        "uuid",
        "run_uuid",
        [
            {
                "name": "afile.pdf",
                "url": "https://example.com",
            }
        ],
        "python:3",
        "https://github.com/example",
        "master",
    )

    assert execute_command_mock.call_count == 6
    assert execute_command_mock.call_args_list[0][0][0] == "docker pull python:3"
    assert (
        execute_command_mock.call_args_list[1][0][0]
        == "git clone https://github.com/example gitrepo"
    )
    assert execute_command_mock.call_args_list[2][0][0] == "git checkout master"
    assert execute_command_mock.call_args_list[3][0][0] == "mkdir input"
    assert execute_command_mock.call_args_list[4][0][0] == "mkdir output"
    assert execute_command_mock.call_args_list[5][0][0].startswith("docker run --rm")

    assert update_run_status_mock.call_count == 2
    assert update_run_status_mock.call_args_list[0] == call(
        "uuid", "run_uuid", RunStateEnum.RUNNING
    )
    assert update_run_status_mock.call_args_list[1] == call(
        "uuid", "run_uuid", RunStateEnum.COMPLETED
    )

    assert urlretrieve_mock.call_count == 1
    assert urlretrieve_mock.call_args_list[0][0][0] == "https://example.com"
