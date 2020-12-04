#!/bin/bash

# allow variables to be passed in from the container
with-contenv

source /etc/services.d/2-postgres/env

# nounset: undefined variable outputs error message, and forces an exit
set -u
# errexit: abort script at first error
set -e
# print command to stdout before executing it:
set -x

chown -R postgres:postgres "$PGDATA"

if [ -z "$(ls -A "$PGDATA")" ]; then
    gosu postgres initdb
    sed -ri "s/^#(listen_addresses\s*=\s*)\S+/\1'*'/" "$PGDATA"/postgresql.conf

    : ${POSTGRES_USER:="postgres"}
    : ${POSTGRES_DB:=$POSTGRES_USER}

    if [ "$POSTGRES_PASSWORD" ]; then
      pass="PASSWORD '$POSTGRES_PASSWORD'"
      authMethod=md5
    else
      echo "==============================="
      echo "!!! NO PASSWORD SET !!! (Use \$POSTGRES_PASSWORD env var)"
      echo "==============================="
      pass=
      authMethod=trust
    fi
    echo


    if [ "$POSTGRES_DB" != 'postgres' ]; then
      createSql="CREATE DATABASE $POSTGRES_DB;"
      echo $createSql | gosu postgres postgres --single -jE
      echo

      createSql="CREATE DATABASE accountservice;"
      echo $createSql | gosu postgres postgres --single -jE
      echo

      createSql="CREATE DATABASE workflowservice;"
      echo $createSql | gosu postgres postgres --single -jE
      echo

      createSql="CREATE DATABASE appservice;"
      echo $createSql | gosu postgres postgres --single -jE
      echo
    fi

    if [ "$POSTGRES_USER" != 'postgres' ]; then
      op=CREATE
    else
      op=ALTER
    fi

    userSql="$op USER $POSTGRES_USER WITH SUPERUSER $pass;"
    echo $userSql | gosu postgres postgres --single -jE
    echo

    gosu postgres pg_ctl -D "$PGDATA" \
        -o "-c listen_addresses=''" \
        -w start

    echo

    gosu postgres pg_ctl -D "$PGDATA" -m fast -w stop

    { echo; echo "host all all 0.0.0.0/0 $authMethod"; } >> "$PGDATA"/pg_hba.conf
fi

if [ -z "$(ls -A "/opt/openfido-workflow-service/.worker-env")" ]; then
  nohup exec gosu postgres postgres &
  POSTGRES_PID=$!

  cd /opt/openfido-auth-service
  source /etc/services.d/3-openfido-auth-service/env

  export ADMIN_EMAIL=${ADMIN_EMAIL:-'admin@example.com'}
  export ADMIN_PASSWORD=${ADMIN_PASSWORD:-'1234567890'}

  flask db upgrade

  flask shell <<END
from app import models, services
u = services.create_user('${ADMIN_EMAIL}','${ADMIN_PASSWORD}','admin','user')
u.is_system_admin = True
models.db.session.commit()
END

  cd /opt/openfido-app-service
  source /etc/services.d/5-openfido-app-service/env

  flask db upgrade

  invoke create-application-key -n "react client" -p REACT_CLIENT | sed 's/^/export /' > /opt/openfido-client/.env

  cd /opt/openfido-workflow-service
  source /etc/services.d/4-openfido-workflow-service/env

  flask db upgrade

  invoke create-application-key -n "local worker" -p PIPELINES_WORKER | sed 's/^/export WORKER_/' > /opt/openfido-workflow-service/.worker-env
  invoke create-application-key -n "local client" -p PIPELINES_CLIENT | sed 's/^/export WORKFLOW_/' > /opt/openfido-app-service/.env

  nohup rabbitmq-server start &
  RABBIT_PID=$!

  sleep 10

  rabbitmqctl start_app

  rabbitmqctl add_vhost api-queue
  echo 'rabbit-password' | rabbitmqctl add_user 'rabbit-user'
  rabbitmqctl set_permissions -p "api-queue" "rabbit-user" ".*" ".*" ".*"

  kill $RABBIT_PID
  kill $POSTGRES_PID
fi
