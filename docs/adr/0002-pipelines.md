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

