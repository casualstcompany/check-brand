UGC_SERVICE_PATH=
UGC_COMPOSE_FILE=docker-compose.dev.yml
UGC_ENV_FILE=ugc.example.env

ugc_full_run: ugc_build_up ugc_upgrade

ugc_build:
	docker compose -f $(UGC_SERVICE_PATH)$(UGC_COMPOSE_FILE) --env-file $(UGC_SERVICE_PATH)$(UGC_ENV_FILE)  build -d

ugc_up:
	docker compose -f $(UGC_SERVICE_PATH)$(UGC_COMPOSE_FILE) --env-file $(UGC_SERVICE_PATH)$(UGC_ENV_FILE) up -d

ugc_build_up:
	docker compose -f $(UGC_SERVICE_PATH)$(UGC_COMPOSE_FILE) --env-file $(UGC_SERVICE_PATH)$(UGC_ENV_FILE) up -d --build

ugc_upgrade:
	docker compose -f $(UGC_SERVICE_PATH)$(UGC_COMPOSE_FILE) --env-file $(UGC_SERVICE_PATH)$(UGC_ENV_FILE) exec service alembic upgrade head

dev_ugc_autogenerate_alembic:
	docker compose -f $(UGC_SERVICE_PATH)$(UGC_COMPOSE_FILE) --env-file $(UGC_SERVICE_PATH)$(UGC_ENV_FILE) exec service alembic revision --autogenerate -m "updated"

dev_ugc_up:
	docker compose -f $(UGC_SERVICE_PATH)$(UGC_COMPOSE_FILE) --env-file $(UGC_SERVICE_PATH)$(UGC_ENV_FILE) up

###############
#    TESTS    #
###############

dev_ugc_test:
	docker compose -f $(UGC_SERVICE_PATH)tests/docker compose.yml --env-file $(UGC_SERVICE_PATH)tests/.test.env down
	docker compose -f $(UGC_SERVICE_PATH)tests/docker compose.yml --env-file $(UGC_SERVICE_PATH)tests/.test.env up --build