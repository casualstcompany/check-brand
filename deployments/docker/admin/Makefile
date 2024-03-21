ADMIN_SERVICE_PATH=
ADMIN_COMPOSE_FILE=docker-compose.dev.yml
ADMIN_ENV_FILE=admin.example.env

admin_full_run: admin_up_build

admin_build:
	docker compose -f $(ADMIN_SERVICE_PATH)$(ADMIN_COMPOSE_FILE) --env-file $(ADMIN_SERVICE_PATH)$(ADMIN_ENV_FILE)  build -d

admin_up:
	docker compose -f$(ADMIN_SERVICE_PATH)$(ADMIN_COMPOSE_FILE) --env-file $(ADMIN_SERVICE_PATH)$(ADMIN_ENV_FILE) up -d

admin_up_build:
	docker compose -f $(ADMIN_SERVICE_PATH)$(ADMIN_COMPOSE_FILE) --env-file $(ADMIN_SERVICE_PATH)$(ADMIN_ENV_FILE) up -d --build

dev_admin_admin_panel_makemigrations:
	docker compose -f $(ADMIN_SERVICE_PATH)$(ADMIN_COMPOSE_FILE) --env-file $(ADMIN_SERVICE_PATH)$(ADMIN_ENV_FILE) exec admin python manage.py makemigrations

dev_admin_admin_panel_generateproto:
	docker compose -f $(ADMIN_SERVICE_PATH)$(ADMIN_COMPOSE_FILE) --env-file $(ADMIN_SERVICE_PATH)$(ADMIN_ENV_FILE) exec admin python manage.py generateproto

dev_admin_admin_panel_create_user:
	docker compose -f $(ADMIN_SERVICE_PATH)$(ADMIN_COMPOSE_FILE) --env-file $(ADMIN_SERVICE_PATH)$(ADMIN_ENV_FILE) exec admin python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"

dev_admin_admin_panel_grpc_generate_ugc_protobuf:
	docker compose -f $(ADMIN_SERVICE_PATH)$(ADMIN_COMPOSE_FILE) --env-file $(ADMIN_SERVICE_PATH)$(ADMIN_ENV_FILE) exec admin python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/auth_by_grpc/protobufs/auth_grpc.proto
	#docker compose -f $(ADMIN_SERVICE_PATH)$(ADMIN_COMPOSE_FILE) --env-file $(ADMIN_SERVICE_PATH)$(ADMIN_ENV_FILE) exec admin python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/grps_clients/ugc/protobufs/ugc_grpc.proto

dev_admin_test:
	docker compose -f $(ADMIN_SERVICE_PATH)tests/functional/docker compose.yml up --build