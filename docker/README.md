Docker Provisioning
===================

This directory contains a Dockerfile of a self contained OpenFido installation.
You can download and use this directly from docker hub:

    docker run -p 127.0.0.1:80:8000 aoeuaoe/openfido

Visit http://127.0.0.1 and login with username `admin@example.com` and
password `1234567890`.

Building
--------

    docker build --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t openfido .
