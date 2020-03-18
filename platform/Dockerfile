FROM python:3.8

ARG REQUIREMENTS=requirements.txt

WORKDIR /app
COPY requirements.txt /app

RUN echo "Install project requirements"
RUN pip3 install -r ${REQUIREMENTS} > /dev/null

COPY . /app

CMD [ "python", "ingest.py" ]