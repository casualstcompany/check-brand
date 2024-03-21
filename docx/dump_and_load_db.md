# Dump and Load to Postgres

1. Делаем Dump

```bash
docker exec <service_name> pg_dump --column-inserts --data-only  -n <schema_1> -n <schema_n...> -p <service_port> --username <username> <name_db> > db_dump.sql
```

2. Загружаем полученные данные

```bash
docker exec -i <service_name> /bin/bash -c "PGPASSWORD=<pass> psql --set ON_ERROR_STOP=on --username <username> <name_db>" < <path_file_dump>
```

### Если вы хотите отключить все триггеры, вы можете использовать:

*Это отключает триггеры для текущего сеанса.*

```bash
SET session_replication_role = replica;
```

*Для повторного включения в том же сеансе:*

```bash
SET session_replication_role = DEFAULT;
```