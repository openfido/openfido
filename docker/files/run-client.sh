#!/bin/bash

cd /opt/openfido-client

source .nvm/nvm.sh
nvm use

serve -l tcp://0.0.0.0:3000 -s build
