Docker Provisioning
===================

This directory contains a Dockerfile of a self contained OpenFido installation.
You can use this directly from docker hub without building it yourself with the
following command:

    docker run docker run --rm \
      -v /tmp:/tmp \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -p 127.0.0.1:5001:5001 \
      -p 127.0.0.1:5002:5002 \
      -p 127.0.0.1:5003:5003 \
      -p 127.0.0.1:3000:3000 \
      openfido

Visit [http://127.0.0.1:3000](http://127.0.0.1:3000) and login with username `admin@example.com` and
password `1234567890`.

Building
--------

To build the image yourself, issue the following command:

    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1

    # Build the docker image, using the SSH private key you use for github
    # access (to access other openslac private repositories)
    docker build --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t openfido .
