# Generating API Keys

Run the following commands from the `openfido-app-service` repository.

Restart the app service after all keys have been generated.

### React Client
Generate an application key for react application to access the app service:

```
docker-compose run --rm app_service \
invoke create-application-key \
-n "react client" \
-p REACT_CLIENT
```

Paste the resulting `API_TOKEN` into the `config/index.js` on `openfido-client`.


### Worker

Generate an access token for a worker to access workflow service:

```
docker-compose run --rm workflow_service \
invoke create-application-key \
-n "local worker" \
-p PIPELINES_WORKER \
| sed 's/^/WORKER_/' > .worker-env
```

This access token will be outputted to the `.worker-env` file.


### App Service as Client to Workflow Service

Generate an access token for the app service client to access workflow service:

```
docker-compose run --rm workflow_service \
invoke create-application-key \
-n "local client" \
-p PIPELINES_CLIENT \
| sed 's/^/WORKFLOW_/' > .env
```

This access token will be outputted to the `.env` file.
