# syntax=docker/dockerfile:1.0.0-experimental
FROM python:3.8-slim as base

# S6 for multiprocess management

ADD https://github.com/just-containers/s6-overlay/releases/download/v2.1.0.2/s6-overlay-amd64-installer /tmp/
RUN chmod u+x /tmp/s6-overlay-amd64-installer && /tmp/s6-overlay-amd64-installer /

VOLUME /var/lib/postgresql/data

# All project dependencies

RUN apt-get update && \
    apt-get install -y gnupg ssh git wget && \
    apt-get clean

# MINIO

RUN mkdir /opt/minio

ADD https://dl.min.io/server/minio/release/linux-ppc64le/minio /tmp/
RUN chmod +x /tmp/minio && mv /tmp/minio /opt/minio

RUN mkdir /etc/services.d/1-minio
RUN mkdir /var/opt/minio
ADD files/run-minio /etc/services.d/1-minio/run

# AUTH SERVER

FROM base as python-deps

# require a private key to access private github repositories
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

FROM python-deps as auth-runtime

COPY openfido-auth-service /opt/openfido-auth-service
COPY --from=python-deps /opt/openfido-auth-service/.venv /opt/openfido-auth-service/.venv
RUN mkdir /etc/services.d/3-openfido-auth-service
ADD files/run-auth-service.sh /etc/services.d/3-openfido-auth-service/run

EXPOSE 5001/tcp

# WORKFLOW SERVER

FROM base as python-deps

# require a private key to access private github repositories
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

FROM auth-runtime as workflow-runtime

COPY openfido-workflow-service /opt/openfido-workflow-service
COPY --from=python-deps /opt/openfido-workflow-service/.venv /opt/openfido-workflow-service/.venv
RUN mkdir /etc/services.d/3-openfido-workflow-service
ADD files/run-workflow-service.sh /etc/services.d/4-openfido-workflow-service/run

EXPOSE 5002/tcp

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
ADD files/entrypoint-postgres.sh /opt/postgres/entrypoint.sh

ENTRYPOINT ["/init"]
