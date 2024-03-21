NOTIFICATION_SERVICE_PATH=
NOTIFICATION_COMPOSE_FILE=docker-compose.dev.yml
NOTIFICATION_ENV_FILE=notification.example.env

notification_full_run: notification_up_build

notification_up:
	docker compose -f $(NOTIFICATION_SERVICE_PATH)$(NOTIFICATION_COMPOSE_FILE) --env-file $(NOTIFICATION_SERVICE_PATH)$(NOTIFICATION_ENV_FILE) up $(d) $(s)

notification_up_build:
	docker compose -f $(NOTIFICATION_SERVICE_PATH)$(NOTIFICATION_COMPOSE_FILE) --env-file $(NOTIFICATION_SERVICE_PATH)$(NOTIFICATION_ENV_FILE) up -d --build


###############
#    ADMIN    #
###############
dev_admin_makemigrations:
	docker compose -f $(NOTIFICATION_SERVICE_PATH)$(NOTIFICATION_COMPOSE_FILE) --env-file $(NOTIFICATION_SERVICE_PATH)$(NOTIFICATION_ENV_FILE) exec admin python manage.py makemigrations

dev_admin_generateproto:
	docker compose -f $(NOTIFICATION_SERVICE_PATH)$(NOTIFICATION_COMPOSE_FILE) --env-file $(NOTIFICATION_SERVICE_PATH)$(NOTIFICATION_ENV_FILE) exec admin python manage.py generateproto

dev_admin_create_user:
	docker compose -f $(NOTIFICATION_SERVICE_PATH)$(NOTIFICATION_COMPOSE_FILE) --env-file $(NOTIFICATION_SERVICE_PATH)$(NOTIFICATION_ENV_FILE) exec admin python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"


###############
#    TESTS    #
###############

dev_notification_test:
	docker compose -f $(NOTIFICATION_SERVICE_PATH)tests/docker compose.yml --env-file $(NOTIFICATION_SERVICE_PATH)tests/.test.env up --build