#!/bin/sh

export FLASK_APP=run.py
export FLASK_RUN_PORT=5001
export FLASK_ENV=production
export PATH=/opt/openfido-auth-service/.venv/bin:$PATH
export SQLALCHEMY_DATABASE_URI="postgresql://postgres:dev-password@localhost/accountservice"
export SECRET_KEY=demo-auth

cd /opt/openfido-auth-service
sh start.sh
