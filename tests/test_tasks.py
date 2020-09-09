from unittest.mock import Mock, call, patch
from urllib.error import URLError

import pytest

from app.models import RunStateEnum
from app.tasks import RunExecutor, execute_pipeline, make_celery
from roles.decorators import ROLES_KEY


def test_make_celery(app):
    celery = make_celery(app)

    @celery.task()
    def add_numbers(a, b):
        return a + b

    assert add_numbers.delay(10, 12).wait() == 22


@patch("app.tasks.urllib_request.urlopen")
def test_update_run_status_error(urlopen_mock, app):
    urlopen_mock.side_effect = URLError("an http error")

    with pytest.raises(URLError):
        executor = RunExecutor("uuid", "run_uuid")
        executor.update_run_status(RunStateEnum.RUNNING)


@patch("app.tasks.urllib_request.urlopen")
def test_update_run_status(urlopen_mock, app):
    executor = RunExecutor("uuid", "run_uuid")
    executor.update_run_status(RunStateEnum.RUNNING)
    assert urlopen_mock.call_count == 1
    request = urlopen_mock.call_args_list[0][0][0]
    assert (
        request.full_url == "http://example.com/v1/pipelines/uuid/runs/run_uuid/state"
    )
    uppered_key = ROLES_KEY[0] + ROLES_KEY[1:].lower()
    assert uppered_key in request.headers.keys()
    assert RunStateEnum.RUNNING.name in request.data.decode("utf-8")


@patch("app.tasks.urllib_request.urlopen")
def test_upload_artifact(urlopen_mock, app):
    executor = RunExecutor("uuid", "run_uuid")
    executor.upload_artifact("example.txt", "tests/sample_db.py")
    assert urlopen_mock.call_count == 1
    request = urlopen_mock.call_args_list[0][0][0]
    assert request.full_url.endswith("run_uuid/artifacts?name=example.txt")
    uppered_key = ROLES_KEY[0] + ROLES_KEY[1:].lower()
    assert uppered_key in request.headers.keys()


class ReturnValue:
    def __init__(self, value, stdout="", stderr=""):
        self.returncode = value
        self.stdout = stdout.encode("ascii")
        self.stderr = stderr.encode("ascii")


@patch("app.tasks.subprocess.run")
def test_run_failure(run_mock, app):
    executor = RunExecutor("uuid", "run_uuid")
    executor.update_run_output = Mock()

    run_mock.return_value = ReturnValue(1)

    with pytest.raises(ValueError):
        executor.run("a command", "/a/dir")

    run_mock.assert_called_once_with(
        ["a", "command"], cwd="/a/dir", capture_output=True
    )
    executor.update_run_output.assert_called()


@patch("app.tasks.subprocess.run")
def test_run(run_mock, app):
    executor = RunExecutor("uuid", "run_uuid")
    executor.update_run_output = Mock()

    run_mock.return_value = ReturnValue(0)

    executor.run("a command", "/a/dir")
    run_mock.assert_called_once_with(
        ["a", "command"], cwd="/a/dir", capture_output=True
    )
    executor.update_run_output.assert_called()


@patch("app.tasks.RunExecutor._put")
def test_update_run_output(request_mock, app):
    executor = RunExecutor("uuid", "run_uuid")

    executor.update_run_output("stdout", "stderr")
    request_mock.assert_called_once_with(
        "console", {"std_out": "\nstdout", "std_err": "\nstderr"}
    )

    # extra calls add data
    request_mock.reset_mock()
    executor.update_run_output("more", "and more")
    request_mock.assert_called_once_with(
        "console", {"std_out": "\nstdout\nmore", "std_err": "\nstderr\nand more"}
    )

    # calls that makes no call
    request_mock.reset_mock()
    executor.update_run_output("", "")
    assert not request_mock.called


@patch("app.tasks.RunExecutor.update_run_output")
@patch("app.tasks.RunExecutor.update_run_status")
@patch("app.tasks.RunExecutor.run")
@patch("os.path.exists")
def test_execute_pipeline_no_openfido(
    exists_mock,
    run_mock,
    update_run_status_mock,
    update_run_output_mock,
    app,
):
    exists_mock.return_value = False

    execute_pipeline(
        "uuid",
        "run_uuid",
        [],
        "python:3",
        "https://github.com/example",
        "master",
    )

    assert run_mock.call_count == 3
    assert run_mock.call_args_list[0][0][0] == "docker pull python:3"
    assert (
        run_mock.call_args_list[1][0][0]
        == "git clone https://github.com/example gitrepo"
    )
    assert run_mock.call_args_list[2][0][0] == "git checkout master"

    assert update_run_status_mock.call_count == 2
    assert update_run_status_mock.call_args_list[0] == call(RunStateEnum.RUNNING)
    assert update_run_status_mock.call_args_list[1] == call(RunStateEnum.FAILED)


@patch("app.tasks.RunExecutor.update_run_output")
@patch("app.tasks.RunExecutor.update_run_status")
@patch("app.tasks.RunExecutor.run")
@patch("os.path.exists")
@patch("app.tasks.urllib_request.urlretrieve")
def test_execute_pipeline_urlerror(
    retrieve_mock,
    exists_mock,
    run_mock,
    update_run_status_mock,
    update_run_output_mock,
    app,
):
    update_run_status_mock.side_effect = URLError("an error")

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

    assert update_run_status_mock.call_count == 2
    assert update_run_status_mock.call_args_list[0] == call(RunStateEnum.RUNNING)
    assert update_run_status_mock.call_args_list[1] == call(RunStateEnum.FAILED)


@patch("app.tasks.RunExecutor.update_run_output")
@patch("app.tasks.RunExecutor.update_run_status")
@patch("app.tasks.RunExecutor.run")
@patch("os.path.exists")
@patch("app.tasks.urllib_request.urlretrieve")
def test_execute_pipeline_valueerror(
    retrieve_mock,
    exists_mock,
    run_mock,
    update_run_status_mock,
    update_run_output_mock,
    app,
):
    run_mock.side_effect = ValueError("an error")

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

    assert update_run_status_mock.call_count == 2
    assert update_run_status_mock.call_args_list[0] == call(RunStateEnum.RUNNING)
    assert update_run_status_mock.call_args_list[1] == call(RunStateEnum.FAILED)


@patch("app.tasks.RunExecutor.update_run_output")
@patch("app.tasks.RunExecutor.update_run_status")
@patch("app.tasks.RunExecutor.upload_artifact")
@patch("app.tasks.RunExecutor.run")
@patch("os.path.exists")
@patch("os.listdir")
@patch("os.path.isfile")
@patch("app.tasks.urllib_request.urlretrieve")
def test_execute_pipeline(
    retrieve_mock,
    isfile_mock,
    listdir_mock,
    exists_mock,
    run_mock,
    upload_artifact_mock,
    update_run_status_mock,
    update_run_output_mock,
    app,
):
    exists_mock.return_value = True
    listdir_mock.return_value = ["output.txt"]
    isfile_mock.return_value = False

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

    assert run_mock.call_count == 6
    assert run_mock.call_args_list[0][0][0] == "docker pull python:3"
    assert (
        run_mock.call_args_list[1][0][0]
        == "git clone https://github.com/example gitrepo"
    )
    assert run_mock.call_args_list[2][0][0] == "git checkout master"
    assert run_mock.call_args_list[3][0][0] == "mkdir input"
    assert run_mock.call_args_list[4][0][0] == "mkdir output"
    assert run_mock.call_args_list[5][0][0].startswith("docker run --rm")

    assert update_run_status_mock.call_count == 2
    assert update_run_status_mock.call_args_list[0] == call(RunStateEnum.RUNNING)
    assert update_run_status_mock.call_args_list[1] == call(RunStateEnum.COMPLETED)

    assert retrieve_mock.call_count == 1
    assert retrieve_mock.call_args_list[0][0][0] == "https://example.com"

    assert upload_artifact_mock.call_count == 1
    assert upload_artifact_mock.call_args_list[0][0][0] == "output.txt"
