# Openfido-utils

Summary: Common [Flask](https://flask.palletsprojects.com/en/1.1.x/) blueprints and database structers shared between openfido-workflow-service and openfido-app-service.

## Vocabulary

 * Application = an HTTP client that is authorized to access a REST endpoint.
 * Application System Permission = an assignment of an Application to a specific System Permission.
 * System Permission = a specific operation that an application is allowed to perform.

## Architectural Decision Records

* [1. Record architecture decisions](docs/adr/0001-record-architecture-decisions.md)
* [2. Migrate from openfido-workflow-service](docs/adr/0002-migrate-from-openfido-workflow-service.md)

## Development

This package includes a subset of libraries for role-based application
authentication. To use it, simply include this library in your project's
dependencies:

Configure your application to use your application's specific application roles:

    from enum import IntEnum, unique

    @unique
    class ExamplePermissions(IntEnum):
        """ Permissions used for Flask endpoints """

        ROLE_1 = 1
        ROLE_2 = 2

Make sure that your application's [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/) configuration includes the tables used to manage these roles.

    # file that sets up 'db':
    from application_roles.models import db as roles_db

    # import your own models
    from .models import db

Finally, make a decorator to enforce these permissions in your views:

    from application_roles.decorators import make_permission_decorator

    permissions_required = make_permission_decorator(ExamplePermissions)

    @permissions_required([ExamplePermissions.ROLE_1])
    @route("/protected_route")
    def protected_route():
        return 'private info'


HTTP clients must then pass a `Workflow-API-Key` header with their api_key. Keys can
be created using the sample code in tasks.py:

    # Create a new Application database record with PIPELINES_CLIENT role.
    invoke create-application-key -n "new app" -p PIPELINES_CLIENT
