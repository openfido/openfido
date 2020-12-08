from invoke import task


@task
def test(c, cov=False, cov_report=False, junit=False, enforce_percent=0):
    """ Run unit tests. """
    command = "pytest --disable-warnings"
    if cov_report:
        command += " --cov-report=html"
    if junit:
        command += " --junitxml=test-results/results.xml"
    if enforce_percent > 0:
        command += f" --cov-fail-under={enforce_percent}"
    if cov or cov_report or junit or enforce_percent:
        command += " --cov app"
    else:
        command += " app tests"

    c.run(command)


@task
def style(c, fix=False):
    """ Run black checks against the codebase. """
    command = "black"
    if not fix:
        command += " --check"

    c.run(f"{command} app tests")


@task
def lint(c, fail_under=0):
    """ Run pylint checks against the codebase """
    command = "pylint --rcfile=.pylintrc"
    if fail_under > 0:
        command += f" --fail-under={fail_under}"

    c.run(f"{command} app")


@task
def precommit(c, fix=False):
    test(c, junit=True, enforce_percent=100)
    style(c, fix=fix)
    lint(c, fail_under=9)


@task
def create_application_key(c, name, permission):
    """ Create an application api_key.

    name = name of the application
    permission = permission to support.
    """
    from app import create_app
    from application_roles.services import create_application
    from app.model_utils import SystemPermissionEnum

    (app, db, _, _) = create_app()
    with app.app_context():
        application = create_application(name, SystemPermissionEnum[permission])
        db.session.commit()
        print(f"API_TOKEN={application.api_key}")


@task
def run_worker(c, input_directory, docker_image, repository_url, repository_branch, repository_script):
    """ Run a pipeline repository locally. This runs a repository with sample
    data provided in `input_directory` using the same logic used by the workflow
    server's celery task.
    """
    from app.tasks import execute_pipeline
    from unittest.mock import patch
    import logging
    import os
    import sys

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logger = logging.getLogger("run_task")

    @patch('app.tasks.get_task_logger')
    @patch('app.tasks.RunExecutor._make_request')
    def fake_execute(make_request_mock, task_logger_mock):
        def note_call(*args, **kwargs):
            print(args)
            return None

        task_logger_mock.return_value = logger
        make_request_mock().side_effect = note_call

        execute_pipeline('pipeline-uuid',
                         'pipeline-run-uuid',
                         [{ "name": f, "url": f"file://{input_directory}/{f}" } for f in os.listdir(input_directory)],
                         docker_image,
                         repository_url,
                         repository_branch,
                         repository_script)
    fake_execute()


@task
def create_pipeline(c, name, docker_image_url, repository_ssh_url, repository_branch='master', repository_script='openfido.sh'):
    """ Create a pipeline. """
    from app import create_app
    from app.pipelines.services import create_pipeline

    (app, db, _, _) = create_app()
    with app.app_context():
        pipeline = create_pipeline({
            'name': name,
            'docker_image_url': docker_image_url,
            'repository_ssh_url': repository_ssh_url,
            'repository_branch': repository_branch,
            'repository_script': repository_script,
        })
        print(pipeline.uuid)
