#!/bin/sh

export FLASK_APP=run.py
export FLASK_RUN_PORT=5002
export FLASK_ENV=production
export PATH=/opt/openfido-workflow-service/.venv/bin:$PATH
export SQLALCHEMY_DATABASE_URI="postgresql://postgres:dev-password@localhost/workflowservice"
export SECRET_KEY=demo-auth

cd /opt/openfido-workflow-service
sh start.sh
