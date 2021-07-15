# 3. deployment

Date: 2020-10-21

## Status

Accepted

## Context

We plan to use AWS as a development/staging environment and as a production environment, on ECS.

## Decision

Use CircleCI for CI, and deploy docker images to AWS ECR for use in deployments.
CircleCI will need to be configured with the following environmental variables
in order to deploy docker images (using [CircleCI's aws-ecr
orb](https://circleci.com/developer/orbs/orb/circleci/aws-ecr)):

- DEV_AWS_ACCESS_KEY_ID
- DEV_AWS_SECRET_ACCESS_KEY
- PROD_AWS_ACCESS_KEY_ID
- PROD_AWS_SECRET_ACCESS_KEY
- AWS_REGION
- AWS_ECR_ACCOUNT_URL

This project's Dockerfile requires access to a privately hosted github project
(openfido-utils). Use [Buildkit](https://docs.docker.com/develop/develop-images/build_enhancements/) on CircleCI to grant SSH access to the docker build processes.

## Consequences

Currently docker-compose only has rudimentary support for Buildkit - and [does
not support passing the --ssh
option](https://github.com/CircleCI-Public/aws-ecr-orb/issues/77). Using
docker-compose locally builds images by explicitly passing the private key -
which is different than the Buildkit `--ssh` option (potentially less secure).
When docker-compose supports Buildkit more fully we should update our local dev
instructions.

We had problems with aws-ecr and aws-ecs orbs - they would pick up the
AWS_ACCESS_KEY_ID values [in different ways](https://github.com/CircleCI-Public/aws-ecs-orb/issues/99) (in short the ecs orb would always
pick up the AWS_ACCESS_KEY_ID even if you explicitly configured it to use a
different variable in the circleci config.). Solution: explicitly name dev/prod
scoped variables within CircleCI.
