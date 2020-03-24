FROM python:3.8

EXPOSE 8100

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

ARG REQUIREMENTS=requirements.txt

WORKDIR /app
COPY requirements.txt /app

RUN echo "Install project requirements"
RUN pip3 install -r ${REQUIREMENTS} > /dev/null

COPY . /app