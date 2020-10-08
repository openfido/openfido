# OpenFIDO App Service

Summary: A service for the [openfido-client](https://github.com/slacgismo/openfido-client), providing organizational access to workflows.

## Vocabulary

# Architecture Decision Records

* [1. Record architecture decisions](docs/adr/0001-record-architecture-decisions.md)
* [2. project structure](docs/adr/0002-project-structure.md)

## Development

This service acts as a frontend to both the [openfido-workflow-service](https://github.com/slacgismo/openfido-workflow-service) and the [openfido-auth-service](https://github.com/slacgismo/openfido-auth-service), and cannot be usefully run without those services configured and setup locally as well. To do this:

 * checkout this repository as well as openfido-workflow-service and openfido-auth-service
 * Run all three docker-compose files to bring up the services.

A convenient way to do this is by setting environmental variables telling
docker-compose which files to use, and where each project is:

    export AUTH_PORT=5002
    # TODO update this when the openfido-auth-service is set up.
    export AUTH_DIR=../loadinsight/presence-account-service
    export WORKFLOW_PORT=5001
    export WORKFLOW_DIR=../openfido-workflow-service
    export COMPOSE_FILE=docker-compose.yml:$WORKFLOW_DIR/docker-compose.yml:$AUTH_DIR/docker-compose.yml

    # Because these repositories make use of private github repositories, they
    # need access to an SSH key that you have configured for github access:
    docker-compose build --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)"

    # Configure the auth service admin account
    cp $AUTH_DIR/.env.example $AUTH_DIR/.env
    vi $AUTH_DIR/.env

    # Initialize all the databases for all the services:
    docker-compose run --rm auth_service flask db upgrade
    docker-compose run --rm workflow_service flask db upgrade 
    docker-compose run --rm app_service flask db

    # Configure the workflow service access tokens:
    docker-compose run --rm workflow_service invoke create-application-key -n "local worker" -p PIPELINES_WORKER | sed 's/^/WORKER_/' > $WORKFLOW_DIR/.worker-env
    docker-compose run --rm workflow_service invoke create-application-key -n "local client" -p PIPELINES_CLIENT | sed 's/^/WORKFLOW_/' > .env

    # bring up all the services!
    docker-compose up

## Deployment

TODO

## Provisioning

TODO
