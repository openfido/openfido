# 3. Authentication

Date: 2020-08-31

## Status

Accepted

## Context

Several applications for OpenFIDO will require APIs with application level
authentication and authorization. These include the pipeline API itself, its
workers, the OpenFIDO services and web client, and the Blob service.

These other services will want to import and use the application roles tables
and functions defined in this project for their own API endpoints, but might
not the pipeline endpoints.

Docs:
 * [OpenFIDO Db/Service Model](https://app.lucidchart.com/documents/edit/5dcaf4fa-7cad-4ce1-9275-ab86110fc2a6/0_0?shared=true)

## Decision

Create a separate 'application roles' package and set of models within this
project that can be imported separately from the pipelines API.
 - [x] Ensure that both logic to enforce a permission (a decorator enforcing a
   requirement of a specific set of SystemPermissions) is included in this
   package.
 - [x] Models are included in such a way that they can be included in an existing
   Alembic database schema (have one central 'db' that is configured by the
   importing app)
 - [x] Create a setup.py file and reference flask project that imports this project
   (basis example for other projects).

## Consequences

Anticipate that importing and using 'application roles' will be trivial to setup
by itself.

We ended up moving this entire source to slacgismo/openfido-utils to share
between multiple repositories. Because that repository is private, we needed to
rework how docker images were built so that they could access the private
repository.
