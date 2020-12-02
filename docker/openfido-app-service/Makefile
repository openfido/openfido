help:
	echo "available targets are: up, down, logs, upgrade-dbs, access-tokens, webflow-api-key, auth-shell"

up: access-tokens webflow-api-key
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f --tail=50

upgrade-dbs:
	docker-compose run --rm auth_service flask db upgrade
	docker-compose run --rm workflow_service flask db upgrade
	docker-compose run --rm app_service flask db upgrade

access-tokens:
	docker-compose run --rm workflow_service invoke create-application-key -n "local worker" -p PIPELINES_WORKER | sed 's/^/WORKER_/' > .worker-env
	docker-compose run --rm workflow_service invoke create-application-key -n "local client" -p PIPELINES_CLIENT | sed 's/^/WORKFLOW_/' > .env

webflow-api-key:
	docker-compose run --rm app_service invoke create-application-key -n "react client" -p REACT_CLIENT

auth-shell:
	docker-compose run --rm auth_service flask shell
