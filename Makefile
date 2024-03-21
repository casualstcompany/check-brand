local_up:
	docker network create -d bridge local_backend_network || true
	docker compose \
	-f deployments/docker/composes/auth_local.yml \
	-f deployments/docker/composes/admin_local.yml \
	-f deployments/docker/composes/handler_local.yml \
	-f deployments/docker/composes/nginx_local.yml \
	--env-file deployments/.env.local up
	

local_build:
	docker compose \
	-f deployments/docker/composes/auth_local.yml \
	-f deployments/docker/composes/admin_local.yml \
	-f deployments/docker/composes/handler_local.yml \
	-f deployments/docker/composes/nginx_local.yml \
	--env-file deployments/.env.local build

dev_up:
	docker network create -d bridge dev_backend_network || true
	docker compose \
	-f deployments/docker/composes/auth_dev.yml \
	-f deployments/docker/composes/admin_dev.yml \
	-f deployments/docker/composes/handler_dev.yml \
	-f deployments/docker/composes/nginx_dev.yml \
	--env-file deployments/.env.dev up

# Auth_service - на время разработки
auth_local_build:
	docker compose \
	-f deployments/docker/composes/auth_local.yml \
	--env-file deployments/.env.local build

auth_local_up:
	docker compose \
	-f deployments/docker/composes/auth_local.yml \
	--env-file deployments/.env.local up

auth_local_migrate:
	docker compose \
	-f deployments/docker/composes/auth_local.yml \
	--env-file deployments/.env.local exec auth_rest flask db migrate


# Admin_service - на время разработки
admin_local_build:
	docker compose \
	-f deployments/docker/composes/admin_local.yml \
	--env-file deployments/.env.local build

admin_local_up:
	docker compose \
	-f deployments/docker/composes/admin_local.yml \
	--env-file deployments/.env.local up

admin_local_makemigrations:
	docker compose \
	-f deployments/docker/composes/admin_local.yml \
	--env-file deployments/.env.local exec admin_service python manage.py makemigrations

admin_local_createsuperuser:
	docker compose \
	-f deployments/docker/composes/admin_local.yml \
	--env-file deployments/.env.local exec admin_service python manage.py createsuperuser

admin_local_dump:
	docker compose \
	-f deployments/docker/composes/admin_local.yml \
	--env-file deployments/.env.local exec admin_service python manage.py dumpdata --exclude auth.permission > db.json


# Admin_service - на время разработки
handler_local_build:
	docker compose \
	-f deployments/docker/composes/handler_local.yml \
	--env-file deployments/.env.local build

handler_local_up:
	docker compose \
	-f deployments/docker/composes/handler_local.yml \
	--env-file deployments/.env.local up