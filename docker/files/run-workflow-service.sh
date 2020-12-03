#!/bin/sh

export FLASK_APP=run.py
export FLASK_RUN_PORT=5002
export FLASK_ENV=production
export PATH=/opt/openfido-workflow-service/.venv/bin:$PATH
export SQLALCHEMY_DATABASE_URI="postgresql://postgres:dev-password@localhost/workflowservice"
export SECRET_KEY=demo-workflow
export CELERY_BROKER_URL="amqp://rabbit-user:rabbit-password@localhost/api-queue"
export S3_ACCESS_KEY_ID=minio_access_key
export S3_SECRET_ACCESS_KEY=minio123
export S3_ENDPOINT_URL="http://localhost:9000"

cd /opt/openfido-workflow-service
sh start.sh
