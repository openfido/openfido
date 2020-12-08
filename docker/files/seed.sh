#!/bin/bash

# allow variables to be passed in from the container
with-contenv

source /opt/postgres/env

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

if [ -z "$(ls -A "/opt/app-keys/react-client")" ]; then
  nohup exec gosu postgres postgres &
  POSTGRES_PID=$!

  cd /opt/openfido-auth-service
  source /opt/openfido-auth-service/env

  export ADMIN_EMAIL=${ADMIN_EMAIL:-'admin@example.com'}
  export ADMIN_PASSWORD=${ADMIN_PASSWORD:-'1234567890'}

  flask db upgrade

  invoke create-user -e "${ADMIN_EMAIL}" -p "${ADMIN_PASSWORD}" -f Admin -l User --is-system-admin
  ORG_UUID=$(invoke create-organization -n "OpenFIDO" -e "${ADMIN_EMAIL}")

  cd /opt/openfido-workflow-service
  source /opt/openfido-workflow-service/env

  flask db upgrade

  invoke create-application-key -n "local worker" -p PIPELINES_WORKER | sed 's/^/export WORKER_/' > /opt/app-keys/worker-client
  invoke create-application-key -n "local client" -p PIPELINES_CLIENT | sed 's/^/export WORKFLOW_/' > /opt/app-keys/pipelines-client
  EXAMPLE_UUID=$(invoke create-pipeline -n "Example" -e master -p openfido.sh -e "python:3" -r "https://github.com/PresencePG/presence-pipeline-example.git" )
  ABSORPTION_UUID=$(invoke create-pipeline -n "Absorption" -e master -p openfido.sh -e "slacgrip/master:200527" -r "https://github.com/PresencePG/grip-absorption-pipeline.git" )
  ANTICIPATION_UUID=$(invoke create-pipeline -n "Anticipation" -e master -p openfido.sh -e "slacgrip/master:200527" -r "https://github.com/PresencePG/grip-anticipation-pipeline.git" )
  RECOVERY_UUID=$(invoke create-pipeline -n "Recovery" -e master -p openfido.sh -e "slacgrip/master:200527" -r "https://github.com/PresencePG/grip-recovery-pipeline.git" )

  cd /opt/openfido-app-service
  source /opt/openfido-app-service/env

  flask db upgrade

  invoke create-application-key -n "react client" -p REACT_CLIENT | sed 's/^.*=\(.*\)$/export const API_TOKEN="\1"/' > /opt/app-keys/react-client
  invoke create-organization-pipeline -o $ORG_UUID -p $EXAMPLE_UUID
  invoke create-organization-pipeline -o $ORG_UUID -p $ABSORPTION_UUID
  invoke create-organization-pipeline -o $ORG_UUID -p $ANTICIPATION_UUID
  invoke create-organization-pipeline -o $ORG_UUID -p $RECOVERY_UUID

  nohup rabbitmq-server start &
  RABBIT_PID=$!

  mkdir /var/run/rabbitmq
  echo $RABBIT_PID > /var/run/rabbitmq/server.pid

  rabbitmqctl wait /var/run/rabbitmq/server.pid
  rabbitmqctl start_app
  rabbitmqctl add_vhost api-queue
  echo 'rabbit-password' | rabbitmqctl add_user 'rabbit-user'
  rabbitmqctl set_permissions -p "api-queue" "rabbit-user" ".*" ".*" ".*"

  kill $RABBIT_PID
  kill $POSTGRES_PID
fi

# On every build we need to configure the react api token on the off chance it changed:
cd /opt/openfido-client
cp /opt/app-keys/react-client /opt/openfido-client/src/config/reactclient.js
. .nvm/nvm.sh
nvm use
npm run build
