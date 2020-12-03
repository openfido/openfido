#!/bin/bash

source $PWD/env

cd /opt/openfido-workflow-service
celery -A app.worker worker -l DEBUG
