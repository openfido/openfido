# syntax=docker/dockerfile:1.0.0-experimental
FROM python:3.8-slim as base

# S6 for multiprocess management

ADD https://github.com/just-containers/s6-overlay/releases/download/v2.1.0.2/s6-overlay-amd64-installer /tmp/
RUN chmod u+x /tmp/s6-overlay-amd64-installer && /tmp/s6-overlay-amd64-installer /

VOLUME /var/lib/postgresql/data

# All project dependencies

RUN apt-get update && \
    apt-get install -y gnupg ssh git wget

# AUTH DEPS

FROM base as auth-deps

ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN mkdir /opt/openfido-auth-service
ADD openfido-auth-service/Pipfile /opt/openfido-auth-service
ADD openfido-auth-service/Pipfile.lock /opt/openfido-auth-service
RUN pip install pipenv
RUN --mount=type=ssh cd /opt/openfido-auth-service && PIPENV_VENV_IN_PROJECT="enabled" pipenv install --dev --deploy

# WORKFLOW DEPS

FROM base as workflow-deps

ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN mkdir /opt/openfido-workflow-service
ADD openfido-workflow-service/Pipfile /opt/openfido-workflow-service
ADD openfido-workflow-service/Pipfile.lock /opt/openfido-workflow-service
RUN pip install pipenv
RUN --mount=type=ssh cd /opt/openfido-workflow-service && PIPENV_VENV_IN_PROJECT="enabled" pipenv install --dev --deploy

# APP SERVER

FROM base as app-deps

ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN mkdir /opt/openfido-app-service
ADD openfido-app-service/Pipfile /opt/openfido-app-service
ADD openfido-app-service/Pipfile.lock /opt/openfido-app-service
RUN pip install pipenv
RUN --mount=type=ssh cd /opt/openfido-app-service && PIPENV_VENV_IN_PROJECT="enabled" pipenv install --dev --deploy

# AUTH, WORKFLOW, WORKER, APP 

FROM base as services

## AUTH

COPY openfido-auth-service /opt/openfido-auth-service
COPY --from=auth-deps /opt/openfido-auth-service/.venv /opt/openfido-auth-service/.venv
RUN mkdir /etc/services.d/3-openfido-auth-service
ADD files/auth-env /etc/services.d/3-openfido-auth-service/env
ADD files/run-auth-service.sh /etc/services.d/3-openfido-auth-service/run

EXPOSE 5001/tcp

## WORKER

COPY openfido-workflow-service /opt/openfido-workflow-service
COPY --from=workflow-deps /opt/openfido-workflow-service/.venv /opt/openfido-workflow-service/.venv
RUN mkdir /etc/services.d/4-openfido-workflow-service
ADD files/workflow-env /etc/services.d/4-openfido-workflow-service/env
ADD files/run-workflow-service.sh /etc/services.d/4-openfido-workflow-service/run

EXPOSE 5002/tcp

## APP

COPY openfido-app-service /opt/openfido-app-service
COPY --from=app-deps /opt/openfido-app-service/.venv /opt/openfido-app-service/.venv
RUN mkdir /etc/services.d/5-openfido-app-service
ADD files/app-env /etc/services.d/5-openfido-app-service/env
ADD files/run-app-service.sh /etc/services.d/5-openfido-app-service/run

EXPOSE 5003/tcp

## WORKER

ADD https://download.docker.com/linux/debian/gpg /tmp/
RUN cat /tmp/gpg | apt-key add -
RUN echo "deb [arch=amd64] https://download.docker.com/linux/debian buster stable" > /etc/apt/sources.list.d/docker.list
RUN apt update && apt install -y docker-ce
RUN mkdir /etc/services.d/6-openfido-workflow-worker
ADD files/worker-env /etc/services.d/6-openfido-workflow-worker/env
ADD files/run-workflow-worker.sh /etc/services.d/6-openfido-workflow-worker/run

## REACT CLIENT
COPY openfido-client /opt/openfido-client

# MINIO

RUN mkdir /opt/minio

ADD https://dl.min.io/server/minio/release/linux-ppc64le/minio /tmp/
RUN chmod +x /tmp/minio && mv /tmp/minio /opt/minio

RUN mkdir /etc/services.d/1-minio
RUN mkdir /var/opt/minio
ADD files/run-minio /etc/services.d/1-minio/run
ADD files/minio-env /etc/services.d/1-minio/env

EXPOSE 9000/tcp

# RABBITMQ

ADD https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc /tmp/
RUN cat /tmp/rabbitmq-release-signing-key.asc | apt-key add -
RUN apt-get install apt-transport-https
RUN echo "deb https://dl.bintray.com/rabbitmq-erlang/debian buster erlang-22.x" > /etc/apt/sources.list.d/bintray.erlang.list
RUN echo "deb https://dl.bintray.com/rabbitmq/debian buster main" > /etc/apt/sources.list.d/bintray.rabbitmq.list
RUN apt-get update && apt-get install rabbitmq-server -y --fix-missing
RUN mkdir /etc/services.d/0-rabbitmq
ADD files/run-rabbitmq /etc/services.d/0-rabbitmq/run
ADD files/rabbitmq-env /etc/services.d/0-rabbitmq/env

EXPOSE 9000/tcp

# POSTGRES

RUN mkdir /opt/postgres
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update && \
    apt-get install -y gosu tzdata postgresql-common postgresql-12 postgresql-contrib-12 && \
    mkdir /docker-entrypoint-initdb.d && \
    apt-get clean
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
RUN mkdir /etc/services.d/2-postgres
ADD files/run-postgres /etc/services.d/2-postgres/run
ADD files/postgres-env /etc/services.d/2-postgres/env

EXPOSE 5432/tcp

# SEED SCRIPT

ADD files/seed.sh /etc/cont-init.d/1-seed.sh

ENTRYPOINT ["/init"]
