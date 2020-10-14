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
def precommit(c):
    test(c, junit=True, enforce_percent=100)
    style(c)
    lint(c, fail_under=9)


@task
def create_application_key(c, name, permission):
    """ Create an application api_key.

    name = name of the application
    permission = permission to support.
    """
    from app import create_app
    from application_roles.services import create_application
    from app.utils import ApplicationsEnum

    (app, db, _) = create_app()
    with app.app_context():
        application = create_application(name, ApplicationsEnum[permission])
        db.session.commit()
        print(f"API_TOKEN={application.api_key}")
