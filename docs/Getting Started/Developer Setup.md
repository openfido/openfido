# Developer Setup

We will be running the OpenFIDO app, auth, and workflow services on our local machine through `localhost` and serving them via [Docker](http://docker.com) containers.

Download the Docker Desktop client and run it on your machine.

Ensure that you have `npm` and `yarn` installed for the OpenFIDO react client to be run in development.

1.  Start by cloning all repositories needed for the OpenFIDO Application to run on your local machine:

    [OpenFIDO App Service](https://github.com/slacgismo/openfido-app-service) \
    [OpenFIDO Workflow Service](https://github.com/slacgismo/openfido-workflow-service) \
    [OpenFIDO Auth Service](https://github.com/slacgismo/openfido-auth-service) \
    [OpenFIDO Front End Client](https://github.com/slacgismo/openfido-client) \
    OpenFIDO Utils (downloaded via other services)

    The **OpenFIDO App Service** acts as a front end client to both the Workflow Service and the Auth Service.

    The **OpenFIDO Client** will be accessing the API endpoints at the App Service as well as at the Auth Service, at different ports.
   
    You will need to configure **ports** on the OpenFIDO Client to match what is being served by the `docker-compose.yml` and `docker run` on *App Service*. Read on!
   
1.  The *App Service* [`README.md`](https://github.com/slacgismo/openfido-app-service/blob/master/README.md) has clear instructions on how to run all the services via docker containers at once.

    At this time, however, we can make use of shortcuts in the [`Makefile`](https://github.com/slacgismo/openfido-app-service/blob/master/Makefile) to call processes, similarly to what is described in the README.

    From the `Makefile`:
    
    ```
    available targets are: up, down, logs, upgrade-dbs, access-tokens, webflow-api-key, auth-shell
    ````
    
    First, create a build of the docker containers as described in the `docker-compose.yml` on `openfido-app-service`.
    
    ```
    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1
    
    docker-compose build \
    --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/<YOUR_ID_RSA_HERE>)"
    ```
    
    You will need to modify the file path for your RSA-encrypted key in this command in order for the OpenFIDO app service to connect to GitHub via ssh (`<YOUR_ID_RSA_HERE>`) to grab the `openfido-utils` repository.
    
    See latest instructions on how to generate an ssh key for your GitHub account on the [GitHub docs](docs.github.com).
    
    From docs.github.com:
    ```
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```
    
    **IMPORTANT: When prompted to enter a passphrase, please press "Enter" for an empty passphrase.**
    
    Replace `<YOUR_ID_RSA_HERE>` with the file name that you had saved your ssh key on.
    
    Lastly, add this ssh key to your GitHub account that has access to `openfido-utils`.
    
    Run the build command each time any major updates occur to the service that require a rebuild, such as changes to the `Pipfile`.
    
1.  Next, you will need to run database migrations on the containers for all services using `docker-compose.yml` on *App Service*.

    ```
    docker-compose run --rm auth_service flask db upgrade
    docker-compose run --rm workflow_service flask db upgrade 
    docker-compose run --rm app_service flask db upgrade
    ```
    
    OR
    
    ```
    make upgrade-dbs
    ```
   
1.  In order for the services to talk to each other, they will need application keys to be set up in their environments. The section **API Documentation - Generating API Keys** has the updated information to generate these keys for your services and react client.

    You can also run
   
    ```
    make up
    ```
   
    which will generate these tokens for you.
    
    Make you sure copy the `API_TOKEN` outputted from the *"react client"* named key generator via this `make` command.
    
    Paste this copied key into your `config/index.js` on `openfido-client`.
    
    See instructions on the Generating API Keys document - section *React Client*.
    
    You do not need to run this command again, unless you need to regenerate API tokens. Just run `docker-compose up`
    
    ```
    docker-compose up
    ``` 

1.  Your docker containers should now be running in the background.

    Run `make logs` to see the server outputs.
    
    ```
    make logs
    ```

    See a list of the containers running and their ports via `docker container ls`.
    
    ```
    docker container ls | grep app-service
    ```
    
    The port numbers for `openfido-app-service_app_service` and `openfido-app-service_auth_service` are detailed in this output.
    
    Check to make sure that the `config/index.js` on `openfido-client` has `BASE_API_URL_AUTH_DEVELOPMENT` and `BASE_API_URL_APP_DEVELOPMENT` configured to point to these ports on `localhost`.
    
    By default, these are `6000` for `openfido-app-service`, `6001` for `openfido-workflow-service`, and `6002` for `openfido-auth-service`
    
    **IMPORTANT: You will need to change the port for the `openfido-app-service` to something like `8080` in development. Browsers such as Chrome consider this port to be unsafe, and therefore, we cannot serve API responses via the browser at port `6000`.**
    
    Change the port numbers in `openfido-client` at `config/index.js` in order to match what is being served by the `docker-compose.yml` and `docker run`.

1.  Your services are up and running! If you ever need to restart manually, run `docker-compose stop` and then `docker-compose up` again.

    ```
    docker-compose stop
    docker-copmose up
    ```
    
    If you ever need to restart from scratch, remove the containers via `docker-compose down` or `docker-compose rm`.
    
    ```
    docker-compose down
    ```
    
    ```
    docker-compose stop
    docker-compose rm
    ```
    
    After you have run the commands to remove the docker containers, you will need to start by rebuilding the docker containers and running database migrations as in the steps above.
     
    ```
    docker-compose build \
    --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/<YOUR_ID_RSA_HERE>)"
    ```
 
    Re-run database migrations:
    ```
    docker-compose run --rm auth_service flask db upgrade
    docker-compose run --rm workflow_service flask db upgrade 
    docker-compose run --rm app_service flask db upgrade
    ```
    
    OR
    
    ```
    make upgrade-dbs
    ```   

1.  Lastly in the setup for backend services, you will need to create an admin user so that you can log in via the React client UI.

    We will need to hit the auth service endpoints with the correct user authentication in order to login.
    
    Enter in to the `auth_service` backend flask shell to create a new user in the `postgresql` database.
    ```
    docker-compose run --rm auth_service flask shell
    ```

    The `openfido-auth-service` [`README.md`](https://github.com/slacgismo/openfido-auth-service/blob/master/README.md) should have the latest on creating a new user.
    
    Run this from the flask shell:
    
    ```
    from app import models, services
    u = services.create_user('admin@example.com', '1234567890', 'admin', 'user')
    u.is_system_admin = True
    models.db.session.commit()
    ```
    
1.  You should now be able to login and create pipelines via the workflow service that you have pushed up to the docker containers.

    Run `yarn install` and `yarn start` on the react `openfido-client` in order to pull up a development server on `localhost:3000`:
    
    ```
    yarn install
    yarn start
    ```
