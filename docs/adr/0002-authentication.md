# 2. Authentication

Date: 2020-05-28

## Status

In Progress

## Context

A couple of client projects need a simple authentication system. One of the
projects already uses Flask and Postgres, while another is in the design phase.

In the short term we want to have a minimal and functional authentication system
implemented as soon as possible.

In the very long term we hope that this implementation would be reused many
times and to have easily customized drop-in libraries for Flask projects.

## Decision

Create a minimal reference authentication implementation that uses Flask and
Postgres. Include unit tests (hopefully strive for very high code coverage), and
database migrations.

Organize the database logic into a simplified CQRS-inspired style code structure:
 * app/models.py contain all sql models.
 * app/services.py contain all db commands that modify database state.
 * app/queries.py contain all db queries to the database.

Delay any features that aren't in our current project requirements. The kinds of
features that may be addressed in future versions, but not initially:

 * Implement this reference as a [Flask extension](https://flask.palletsprojects.com/en/1.1.x/extensiondev/), and possibly add to the PyPi public repositories.
 * Create a React reference implementation.
 * password resets
 * email account verification
 * permissions
 * multi factor authentication
 * OAuth
 * Expiring tokens
 * Revoking/blacklisting tokens
 * prevent re-use of old passwords

## Consequences

As more projects use this template, we run the risk of creating lots of little
'balls of mud' antipattern.
