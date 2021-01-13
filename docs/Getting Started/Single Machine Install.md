OpenFIDO is made of several microservices (app service, auth service, client, utils, and workflow service). This repository brings all these services together. You can check out each service and how to run them individually under their separate directories in [openfido/docker](https://github.com/slacgismo/openfido/tree/master/docker). 

If you would like a simple setup to see how the app runs locally, you can run the command below on your terminal.</br>
You can also check out this docker command [here](https://github.com/slacgismo/openfido/blob/master/docker/README.md).
```
    docker run --rm \
      -v /tmp:/tmp \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -p 127.0.0.1:5001:5001 \
      -p 127.0.0.1:5002:5002 \
      -p 127.0.0.1:5003:5003 \
      -p 127.0.0.1:9000:9000 \
      -p 127.0.0.1:3000:3000 \
      openfido/openfido
```
## Development Setup
The following documentation is a step-by-step on how to run the services together for local development purposes.  

First, please clone the OpenFIDO repository if you have not already:
```
git clone https://github.com/slacgismo/openfido.git
```

## Backend Setup

Navigate into the openfido-app-service on your terminal.
```
cd docker/openfido-app-service
```

A convenient way to set up these services locally is by setting environmental variables that tell docker-compose which files to use, and where each project is:
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

**IMPORTANT:** When prompted to enter a passphrase, please press "Enter" for an empty passphrase.

Add this ssh key to your GitHub account that has access to openfido-utils.
To do this, sign into your corresponding Github account and navigate to https://github.com/settings/ssh/new. Inside the key body, add your SSH public key. </br>
You will need to remember your private ID RSA for a later step.

If you forget what you named your ssh keys, you can list the file names on your terminal:
```
ls -al ~/.ssh
```
Please note that you will need to run the build command each time any major updates occur to the service that require a rebuild, such as changes to the Pipfile.
```
    touch .worker-env
    touch ../openfido-auth-service/.env
```
Replace <YOUR_ID_RSA_HERE> with the file name where you saved your private ssh key. </br>
```
    docker-compose build --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/<YOUR_ID_RSA_HERE>)"
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
Bring up all the services! </br>
You will only need to run this command to bring up the backend services from now on.
```
    docker-compose up
```

**NOTE:** The local setup of OpenFIDO uses [minIO](https://min.io/) to act as an object storage service. Artifact and input links during a pipeline run are currently configured to navigate to blobstorage:9000. In order to enable the capability of downloading from these links, you will need to edit your /etc/hosts file to add blobstorage as a recognizable url name for localhost. The following are the terminal commands to do this for *nix platform.

```
sudo nano /etc/hosts
```
Next to 127.0.0.1, you should see "localhost". Please type in "blobstorage" after localhost. Then click CTRL + o to save the changes to /etc/hosts, and CTRL + x to exit the file.

## Frontend Setup
Open another tab on your terminal and navigate into openfido-client.
```
    cd ../openfido-client
    npm install
    npm start
```

Navigate to http://localhost:3000/ and sign in with the super admin user. :grin: <br />
For first-time setup, you will need to create an organization under settings. 
