# OpenFIDO Auth Service

A reference authentication server implementation, written in [Flask](https://flask.palletsprojects.com/en/1.1.x/).

[![CircleCI](https://circleci.com/gh/PresencePG/presence-account-service.svg?style=svg&circle-token=a974a5a5a2b8c18d84b39e3212f5bb5bef68109e)](https://circleci.com/gh/PresencePG/presence-account-service)
# Configuration

Flask's app.name is used as JWT the 'iss' issuer key. Be sure to configure an
identifiable name for your application.

The following environmental variables are exposed:

 * `SECRET_KEY`: The [Flask secret key variable](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY). Used as the JWT secret.
 * `SQLALCHEMY_DATABASE_URI`: Database connection string.
 * `SYSTEM_EMAIL`: Email address to use as the 'from address' when emails are sent to users.
 * `EMAIL_DRIVER`: Mail server backend implementation. Each backend has its own settings, see the Mail section. Valid options:
 `null`, and `sendgrid`.

## Email integrations

**Null**: a no-op email integrations. Sends any email to a python logger. To use
this implemetation, set the following environmental variables:
 * `EMAIL_DRIVER`: `null`

**Sendgrid**: Sendgrid web API integrations. Uses Sendgrid's template system to
send emails to users. Additional environmental variables required to use this
implementation:
 * `EMAIL_DRIVER`: `sendgrid`
 * `SENDGRID_API_KEY`: SendGrid [API key](https://sendgrid.com/docs/ui/account-and-settings/api-keys/).
 * `SENDGRID_RESET_TEMPLATE_ID`: SendGrid 'reset email' template id of a [dynamic template](https://sendgrid.com/docs/ui/sending-email/how-to-send-an-email-with-dynamic-transactional-templates/).

# Architecture Decision Records

* [1. Record architecture decisions](docs/adr/0001-record-architecture-decisions.md)
* [2. Authentication](docs/adr/0002-authentication.md)

# Development

The local development environment has been set up with docker compose. Once you
have [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) execute the following commands to setup your local development environment:

    # Copy the .env.example file into .env
    cp .env.example .env

    # Login to an docker instance of the flask app:
    docker-compose run --rm auth_service bash

    # Run database migrations
    flask db upgrade

    # exit the docker instance
    exit

To start the server locally:

    # start both the postgres database, and the flask app:
    docker-compose up

    # visit the app:
    http://localhost:5000/
    
To connect to the database:

    # while docker-compose is running
    docker-compose exec db psql -d accountservices -U postgres
    

To connect to a shell in the auth_service container:
    
    # while docker-compose is running:
    docker-compose exec auth_service bash
    
To connect to a shell in the db container:
    
    # while docker-compose is running:
    docker-compose exec db bash

To run tests, use [invoke](https://pyinvoke.org):

    # Run within the preconfigured docker instance:
    docker-compose run --rm auth_service invoke test

    # with code coverage
    docker-compose run --rm auth_service invoke test --cov-report && open htmlcov/index.html

    # Or if you'd rather run locally
    pipenv install
    pipenv run invoke test

    # to run a lint test
    docker-compose run --rm auth_service invoke lint

    # to check code style
    docker-compose run --rm auth_service invoke style

    # to auto-correct code style errors
    docker-compose run --rm auth_service invoke style --fix

Other tasks are available, in particular the `precommit` task, which mirrors the
tests performed by CircleCI.

Endpoints have been documented with [swagger](https://swagger.io/blog/news/whats-new-in-openapi-3-0/), which is configured to be easily explored in the default `run.py` configuration. When the flask server is running visit http://localhost:5000/apidocs to see documentation and interact with the API directly.
