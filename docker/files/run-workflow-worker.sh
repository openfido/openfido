#!/bin/bash

source $PWD/env
source /opt/openfido-workflow-service/.worker-env

cd /opt/openfido-workflow-service
celery -A app.worker worker -l DEBUG
