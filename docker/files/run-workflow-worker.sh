#!/bin/bash

cd /opt/openfido-workflow-service
source ./worker-env
source /opt/app-keys/worker-client

celery -A app.worker worker -l DEBUG
