# 2. project structure

Date: 2020-10-06

## Status

Accepted

## Context

The OpenFIDO project will mediate access to a workflow service that runs
GridLabD jobs. The frontend React application will need access to these
resources, but only if they have permission to access via an organization.

## Decision

Create a Flask Rest service - since the other microservices in this suite of
services are also Flask based, keep this using the same kind of infrastructure
so that common utilities can be shared (openfido-utils) and the maintenance will
be simplified.

Organize the database logic into a simplified CQRS-inspired style code
structure. Since we anticipate many conceptual resources, each resource will
have its own module:
 * app/RESOURCE/models.py - contains all models for RESOURCE.
 * app/RESOURCE/routes.py - contains all Rest routes specific to RESOURCE.
 * app/RESOURCE/schemas.py - contains all Marshmallow schemas specific to routes of RESOURCE.
 * app/RESOURCE/services.py - all db commands that modify database state.
 * app/RESOURCE/queries.py - all db queries to the database.

Additional libraries we anticipate using:
 * [marshmallow](https://marshmallow.readthedocs.io/en/stable/) will be used since there are many rest api endpoints that will take nested bodies.
 * [alembic](https://alembic.sqlalchemy.org/en/latest/) to manage database schema migrations.

Other thoughts on design:
 * Because HTTP errors are intended for human use via the OpenFIDO client, messages should be verbose - showing both a generic message and specific field validation messages where appropriate.

Use the structure of the [openfido-workflow-service](https://github.com/slacgismo/openfido-workflow-service) project as a reference.

## Consequences
