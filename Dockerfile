FROM python:3.7
RUN apt-get update -qq && \
  apt-get install -y pipenv \
  # for db connectivity
  postgresql-client \
  && \
  apt-get clean

RUN mkdir /opt/app
WORKDIR /opt/app

ADD Pipfile /opt/app/Pipfile
ADD Pipfile.lock /opt/app/Pipfile.lock
RUN pipenv install --system --dev
