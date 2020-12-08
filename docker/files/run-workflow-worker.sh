#!/bin/bash

cd /opt/openfido-workflow-service
source ./worker-env
source ./.worker-env

celery -A app.worker worker -l DEBUG
