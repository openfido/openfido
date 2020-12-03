#!/bin/sh

export FLASK_APP=run.py
export FLASK_RUN_PORT=5003
export FLASK_ENV=production
export PATH=/opt/openfido-app-service/.venv/bin:$PATH
export SQLALCHEMY_DATABASE_URI="postgresql://postgres:dev-password@localhost/appservice"
export SECRET_KEY=demo-auth

cd /opt/openfido-app-service
sh start.sh
