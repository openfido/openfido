# 2. pipelines

Date: 2020-08-18

## Status

Accepted

## Context

A couple of client projects need infrastructure to process GridLabD jobs.

The goal would be that other projects could either include this project as its
own service in their infrastructure, or incorporate it directly into their
Flask-based project.

These kinds of jobs are long running, and produce artifacts that each project
may store in different ways (but primarily S3).

## Decision

Create a Flask Rest service, coupled with Celery for job processing.

Organize the database logic into a simplified CQRS-inspired style code structure:
 * app/models.py contain all sql models.
 * app/services.py contain all db commands that modify database state.
 * app/queries.py contain all db queries to the database.


## Consequences

Initially I'd used manual validation of parameters passed to routes - but as I
implemented more and more of the routes I realized they needed improved
validation (verify that URLs are really URLs, that nested array structures are
I added the [marshmallow library](https://marshmallow.readthedocs.io/en/stable/)
to enforce more consistent validation (and less work!). As a consequence, some
older/simpler routes that I implemented early on aren't validated with
marshmallow, and aren't consistent -- they will be refactored over time to use
marshmallow.
