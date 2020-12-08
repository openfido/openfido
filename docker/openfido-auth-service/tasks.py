from invoke import task


@task
def test(c, cov=False, cov_report=False, junit=False, enforce_percent=0):
    """ Run unit tests. """
    command = "pytest"
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
    test(c, junit=True, enforce_percent=92)
    style(c, fix=fix)
    lint(c, fail_under=9)


@task
def create_user(c, email, password, first_name, last_name, is_system_admin=False):
    """ Create a user. Returns the UUID of the organization. """
    from app import create_app, models, services

    (app, db, _) = create_app()
    with app.app_context():
        user = services.create_user(email, password, first_name, last_name)
        user.is_system_admin = is_system_admin
        models.db.session.commit()
        print(user.uuid)


@task
def create_organization(c, name, email):
    """ Create an organization for a user with 'email'. Returns the UUID of the organization. """
    from app import create_app, models, services, queries

    (app, db, _) = create_app()
    with app.app_context():
        user = queries.find_user_by_email(email)
        organization = services.create_organization(name, user)
        models.db.session.commit()
        print(organization.uuid)
