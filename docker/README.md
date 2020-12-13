Docker Provisioning
===================

This Docker image provides a multi-service docker image that demonstrates the
OpenFido platform.

To run this image directly, use the following command:

    docker run --rm \
      -v /tmp:/tmp \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -p 127.0.0.1:5001:5001 \
      -p 127.0.0.1:5002:5002 \
      -p 127.0.0.1:5003:5003 \
      -p 127.0.0.1:9000:9000 \
      -p 127.0.0.1:3000:3000 \
      openfido/openfido

The system will take a few minutes to bring up the underlying services and seed
the initial system databases.

Visit [http://127.0.0.1:3000](http://127.0.0.1:3000) and login with username `admin@example.com` and
password `1234567890`. Several pipelines are created in an 'OpenFIDO' organization.

Building
--------

To build the image yourself, issue the following command:

    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1

    # Build the docker image, using the SSH private key you use for github
    # access (to access other openslac private repositories)
    docker build --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t openfido/openfido .


Once you've logged into the docker hub account you can push your built images:

    docker push openfido/openfido

Development
-----------

This project can be used for local development for the entire project.

TODO We need to setup a docker-compose.yml that is similar to the
openfido-app-service project's and include the openfido-utils project as a git
subtree.

    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1

    touch .worker-env
    touch openfido-auth-service/.env

    # Build the docker image, using the SSH private key you use for github
    # access (to access other openslac private repositories)
    docker-compose build --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)"

    # Initialize all the databases for all the services:
    docker-compose run --rm auth-service flask db upgrade
    docker-compose run --rm workflow-service flask db upgrade 
    docker-compose run --rm app-service flask db upgrade

    # Configure the workflow service access tokens:
    docker-compose run --rm workflow-service invoke create-application-key -n "local worker" -p PIPELINES_WORKER | sed 's/^/WORKER_/' > .worker-env
    docker-compose run --rm workflow-service invoke create-application-key -n "local client" -p PIPELINES_CLIENT | sed 's/^/WORKFLOW_/' > .workflow-env

    # Obtain the React application key.
    # COPY this to openfido-client/src/config/index.js to the API_TOKEN_DEVELOPMENT variable:
    docker-compose run --rm app-service invoke create-application-key -n "react client" -p REACT_CLIENT

    # Create an super admin user:
    docker-compose run --rm auth-service flask shell
    from app import models, services
    u = services.create_user('admin@example.com', '1234567890', 'admin', 'user')
    u.is_system_admin = True
    models.db.session.commit()

    # bring up all the services!
    docker-compose up


Git Subtree
-----------

This repository contains all the underlying project requirements needed for
local development. One can use it for local development, and share any changes
with the original project. Similarly, any new changes from downstream projects
can be pulled into this project.

Set up your local git project with remotes for each dependent subproject (not
strictly necessary, but makes working with `git subtree` commands more concise):

    git remote add openfido-workflow-service git@github.com:slacgismo/openfido-workflow-service.git
    git remote add openfido-auth-service git@github.com:slacgismo/openfido-auth-service.git
    git remote add openfido-app-service git@github.com:slacgismo/openfido-app-service.git
    git remote add openfido-client git@github.com:slacgismo/openfido-client.git
    git remote add openfido-utils git@github.com:slacgismo/openfido-utils.git


NOTE: To simplify subtree merging be sure to commit any changes to these
projects as individual commits.

### Pulling from upstream projects

To pull in any changes from the original projects to this one, you can use `git
subtree pull`. To pull changes from all dependent projects:

    git subtree pull --prefix=docker/openfido-workflow-service openfido-workflow-service master
    git subtree pull --prefix=docker/openfido-auth-service openfido-auth-service master
    git subtree pull --prefix=docker/openfido-app-service openfido-app-service master
    git subtree pull --prefix=docker/openfido-client openfido-client master
    git subtree pull --prefix=docker/openfido-utils openfido-utils master

### Pushing to original projects

When pushing to the original project, you use `git subtree push` -- you need to
specify the `--prefix` of the original project when pushing. For example,
supposed we are pushing changes to the `docker/openfido-workflow-service` back
to its original project:

    git subtree push --prefix=docker/openfido-workflow-service openfido-workflow-service FEATURE-BRANCH

You can then create a pull request on the original project for the `FEATURE-BRANCH`.
