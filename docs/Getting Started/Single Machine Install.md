OpenFIDO is made of several microservices split into different repositories. You can opt to only run one service at a time. The details for development on each service are documented in their corresponding respositories. 

This documentation is a step-by-step to getting all the services running on your local machine together.

First, please clone the following OpenFIDO repositories into the same directory on your machine:
* [openfido-app-service](https://github.com/slacgismo/openfido-app-service)
* [openfido-auth-service](https://github.com/slacgismo/openfido-auth-service)
* [openfido-utils](https://github.com/slacgismo/openfido-utils)
* [openfido-workflow-service](https://github.com/slacgismo/openfido-workflow-service)
* [openfido-client](https://github.com/slacgismo/openfido-client)

## Backend Setup

Navigate into the openfido-app-service on your terminal.

A convenient way to step up these services locally is by setting environmental variables that tell docker-compose which files to use, and where each project is:
```
    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1
```

Configure the auth service admin account:
```
    cp ../openfido-auth-service/.env.example .auth-env
```

Because these repositories make use of private github repositories, they
need access to an SSH key that you have configured for github access.

See latest instructions on how to generate an ssh key for your GitHub account on the GitHub docs.

From docs.github.com:
```
    ssh-keygen -t ed25519 -C "your_email@example.com"
```

**IMPORTANT:** When prompted to enter a passphrase, please press "Enter" for an empty passphrase.<br />
Replace <YOUR_ID_RSA_HERE> with the file name that you had saved your ssh key on.<br />
Lastly, add this ssh key to your GitHub account that has access to openfido-utils.<br />

Please note that you will need to run the build command each time any major updates occur to the service that require a rebuild, such as changes to the Pipfile.
```
    touch .worker-env
    touch ../openfido-auth-service/.env
    docker-compose build --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)"
```

Initialize all the databases for all the services:
```
    docker-compose run --rm auth-service flask db upgrade
    docker-compose run --rm workflow-service flask db upgrade 
    docker-compose run --rm app-service flask db upgrade
```

Configure the workflow service access tokens:
```
    docker-compose run --rm workflow-service invoke create-application-key -n "local worker" -p PIPELINES_WORKER | sed 's/^/WORKER_/' > .worker-env
    docker-compose run --rm workflow-service invoke create-application-key -n "local client" -p PIPELINES_CLIENT | sed 's/^/WORKFLOW_/' > .env
```

Obtain the React application key:
```
    docker-compose run --rm app-service invoke create-application-key -n "react client" -p REACT_CLIENT
```

Then, copy the React application key to openfido-client/src/config/index.js to the API_TOKEN_DEVELOPMENT variable.

Create a super admin user:
```
    docker-compose run --rm auth-service flask shell
    >>> from app import models, services
    >>> u = services.create_user('admin@example.com', '1234567890', 'admin', 'user')
    >>> u.is_system_admin = True
    >>> models.db.session.commit()
```
Bring up all the services!
```
    docker-compose up
```

## Frontend Setup
Open another tab on your terminal and navigate into openfido-client.
```
    conda create -n venv_ofclient
    conda activate venv_ofclient
    npm install
    npm start
```

Navigate to http://localhost:3000/ and sign in with the super admin user. :grin: <br />
For first-time setup, you will need to create an organization under settings. 
