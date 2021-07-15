# Workflow Service

Summary: A [Flask](https://flask.palletsprojects.com/en/1.1.x/) API server that
offers an ability to execute GridLabD jobs and store the resulting artifacts on
a file server.

## Vocabulary

 * Pipeline = a GridLabD job.
 * Pipeline Run = An execution of a Pipeline.
 * Workflow = A collection of interdependent Pipelines.

## Architectural Decision Records

 * [1. Record architecture decisions](docs/adr/0001-record-architecture-decisions.md)
 * [2. Pipelines](docs/adr/0002-pipelines.md)
 * [3. Authentication](docs/adr/0003-authentication.md)
 * [4. Deployment](docs/adr/0004-deployment.md)

## Development

The local development environment has been set up with docker compose. Once you
have [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) execute the following commands to setup your local development environment:

    # Set up worker configuration:
    cp _worker_env.example .worker-env

    # Build the docker image, using the SSH private key you use for github
    # access (to access other openslac private repositories)
    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1
    docker-compose build --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)"
    # TODO at some point docker-compose will support the "--ssh default" docker
    # parameter - until then we need to pass the key manually :(

    # Login to an docker instance of the flask app:
    docker-compose run --rm workflow-service bash

    # Run database migrations
    flask db upgrade

    # Create worker API token and client API token

    invoke create-application-key -n "local worker" -p PIPELINES_WORKER | sed 's/^/WORKER_/' > .worker-env
    invoke create-application-key -n "local worker" -p PIPELINES_CLIENT

    # exit the docker instance
    exit

To start the server locally:

    # start both the postgres database, and the flask app:
    docker-compose up

    # visit the app:
    http://localhost:5000/

To run tests, use [invoke](https://pyinvoke.org):

    # Run within the preconfigured docker instance:
    docker-compose run --rm workflow-service invoke test

    # with code coverage
    docker-compose run --rm workflow-service invoke --cov-report test

    # Or if you'd rather run locally
    pipenv install
    pipenv run invoke test

Other tasks are available, in particular the `precommit` task, which mirrors the
tests performed by CircleCI. See `invoke -l` for a full list of tasks.

The local docker worker will execute jobs, but requires an API key in order to
update its status (generated in the instructions above).

Endpoints have been documented with [swagger](https://swagger.io/blog/news/whats-new-in-openapi-3-0/), which is configured to be easily explored in the default `run.py` configuration. When the flask server is running visit http://localhost:5000/apidocs to see documentation and interact with the API directly.

## Workers

You can use the `run-worker` invoke task to test repositories. For instance, you
can test the anticipation integration by uploading the 'inputs' of the run to an
input directory and executing the following command:

    invoke run-worker $PWD/inputs 'slacgrip/master:200527' https://github.com/PresencePG/grip-anticipation-pipeline.git master openfido.sh

## Configuration

Common settings used by both server and workers:

 * **CELERY_BROKER_URL** = Location of the [celery broker](https://docs.celeryproject.org/en/stable/userguide/configuration.html#broker-settings).
 * **S3_ACCESS_KEY_ID** = Access key for uploaded artifacts (optional).
 * **S3_SECRET_ACCESS_KEY** = Secret key for uploaded artifacts (optional).
 * **S3_ENDPOINT_URL** = Hostname of the S3 service.
 * **S3_REGION_NAME** = S3 region (default: us-east-1).
 * **S3_BUCKET** = Bucket where uploaded artifacts are kept.

See the [constants.py](app/constants.py) for additional non-configurable
options.


### Server Configuration

Several environmental variables allow this server to be configured.

 * **SECRET_KEY** = See [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY).
 * **SQLALCHEMY_DATABASE_URI** = Database connection string.
 * **CELERY_BROKER_URL** = Location of the [celery broker](https://docs.celeryproject.org/en/stable/userguide/configuration.html#broker-settings).
 * **CELERY_ALWAYS_EAGER** = When True, [execute celery jobs locally](https://docs.celeryproject.org/en/stable/userguide/configuration.html#std:setting-task_always_eager). Useful for development/testing purposes.
 * **MAX_CONTENT_LENGTH** = Configures [maximum upload file byte size](https://flask.palletsprojects.com/en/1.1.x/config/#MAX_CONTENT_LENGTH).

### Worker Configuration

Celery workers only require the following parameters:
 * **WORKER_API_SERVER** = The Workflow API server. Celery workers require access to this Workflow API in
     order to update pipeline run states, and upload artifacts.
 * **WORKER_API_TOKEN** = An application access token to access pipeline run
     endpoints.

To generate a token that a worker may use to interact with the API, use the
following command:

    invoke create-application-key -n "local worker" -p PIPELINES_WORKER

## Deployment

See [openfido terraform docs](https://github.com/slacgismo/openfido/blob/master/terraform/provisioning.md).
