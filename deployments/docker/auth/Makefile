AUTH_COMPOSE_FILE=deployments/docker/auth/local.yml
AUTH_ENV_FILE=deployments/docker/auth/.env.auth.local

auth_build:
	docker compose -f $(AUTH_COMPOSE_FILE) --env-file $(AUTH_ENV_FILE)  build

auth_up:
	docker compose -f $(AUTH_COMPOSE_FILE) --env-file $(AUTH_ENV_FILE) up -d

auth_db_migrate:
	docker compose -f $(AUTH_COMPOSE_FILE) --env-file $(AUTH_ENV_FILE) exec service flask db migrate
