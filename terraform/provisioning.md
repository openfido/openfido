# Provisioning

Run terragrunt for a specific environment to create AWS:

TODO show commands needed to create environment.

TODO include docs for configuring the AWS --profile setting for the account.

# Configuration

Once the infrastructure has been stood up, the databases and initial accounts
need to be initialized.
 * Several services require that an [application token](https://github.com/slacgismo/openfido-utils)
   is passed to the API in order to access it. These need to be generated.
 * An initial account needs to be created in order to administer the openfido website.

TODO how to set up the ec2 instance for tunnelling access to the postgres database.

Get the ec2 hostname, PEM identity file for ec2 instance, and postgres server hostname.

Set up your local .ssh/config to forward connections to the RDS database
instance that is used by all services:

```
Host openfido-tunnel
  User     ec2-user
  HostName *** IP ADDRESS ***
	IdentityFile ~/.ssh/*** PEM FILE ***
	LocalForward 5432 *** RDS HOSTNAME ***
```

Copy the PEM file to your ssh configuration directory, and update its permissions:

```
chmod 600 ~/.ssh/*** PEM FILE ***
```

You should then be able to SSH to the EC2 instance to establish a tunnel to the
RDS database. Set up the environmental variables on your local projects to
access the databases to create application tokens and admin accounts:

```
ssh openfido-tunnel
```

For each project, enter the pipenv shell and configure your local environment to
match the remote environment:

```
pipenv shell
pipenv install --dev
export FLASK_APP=run.py
export FLASK_ENV=development
export SECRET_KEY='*** TERRAFORM GENERATED SECRET KEY ***'
export DATABASE_PASSWORD='*** TERRAFORM GENERATED DATABASE PASSWORD ***'
```

Service databases
-----------------

Create databases for each service if they don't already exist:

```
# create databases:
export PGDATABASE=appservice
export PGUSER=openfido
export PGHOST=localhost

psql

create database authservice;
create database workflowservice;
```

App service
-----------

The app service APIs require an application token. Generate one for the
openfido-client repository:

```
cd openfido-app-service

# ENTER PIPENV AS DESCRIBED ABOVE

export SQLALCHEMY_DATABASE_URI="postgresql://openfido:$DATABASE_PASSWORD@localhost/appservice"
invoke create-application-key -n "react client" -p REACT_CLIENT
```


Auth service
------------

The auth service requires an application token to access its API. Generate one,
and update the terraform variables for the application service.

Also, an administrator account needs to be created for the system. Pick the
username and password for this account and create it:

```
cd openfido-auth-service

# ENTER PIPENV AS DESCRIBED ABOVE

export SQLALCHEMY_DATABASE_URI="postgresql://openfido:$DATABASE_PASSWORD@localhost/authservice"

flask db upgrade

flask shell
from app import models, services
u = services.create_user('*** PICK ADMIN EMAIL ***','*** CREATE A NEW PASSWORD ***','admin','user')
u.is_system_admin = True
models.db.session.commit()
```

TODO Which terraform variables need to be updated for the app service? Document here.

Workflow service
----------------

The workflow service APIs requires specific application tokens for [workflow workers](https://github.com/slacgismo/openfido-workflow-service#workers) and
standard applications (eg, the app service).

```
cd openfido-workflow-service

# ENTER PIPENV AS DESCRIBED ABOVE

export SQLALCHEMY_DATABASE_URI="postgresql://openfido:$DATABASE_PASSWORD@localhost/workflowservice"

flask db upgrade

invoke create-application-key -n "local worker" -p PIPELINES_WORKER
invoke create-application-key -n "local worker" -p PIPELINES_CLIENT
```

TODO Which terraform variables need to be updated for the app service? Document here.

Openfido client
---------------

Create a new pull request on the openfido-client with the [updated application token](https://github.com/slacgismo/openfido-client/blob/master/src/config/index.js#L13-L15)
for the specific environment this system is for. Deploy the openfido-client.

- set API_TOKEN_* of your environment to the value of the application token you generated for the app service.
- set BASE_API_URL_APP_* to the hostname of app service
- set BASE_API_URL_AUTH_* to the hostname of auth service

# Continuous Deployment

Continuous Deployment and integration of the other projects is handled via
CircleCI. To set this up, you need to provide AWS credentials and an ECR
credentials via the Circle CI environmental variables for each project.

TODO Where to obtain ECR hostname and AWS credentials.
