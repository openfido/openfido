# 2. Migrate from openfido-workflow-service

Date: 2020-10-01

## Status

Accepted

## Context

Application role-based Flask authentication is needed for more than one
microservice. An implementation already exists in openfido-workflow-service.

## Decision

Move the roles based blueprint and database migrations into this repository so
that it can be shared across many projects.

## Consequences

The dependencies used to implement this require Flask/SQLAlchemy/Alembic stack.
Probably not a bad thing.
