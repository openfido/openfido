FROM python:3.8-slim as base

FROM base as python-deps

RUN apt-get update -qq && apt-get install -y ssh git

# require a private key to access private github repositories
ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

ADD Pipfile .
ADD Pipfile.lock .
RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

FROM base as runtime

RUN apt-get update -qq && \
  apt-get install -y pipenv \
  # for db connectivity
  postgresql-client \
  && \
  apt-get clean

RUN mkdir /opt/app
WORKDIR /opt/app

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

COPY . .
