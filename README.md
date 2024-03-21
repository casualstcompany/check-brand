# Бэкенд сервиса CheckBrand

## Развертывание на локальном сервере

```bash
cp -R protobufs auth_protobufs
cp -R protobufs admin_protobufs
```

```bash
sed 's/EXAMPLE_/LOCAL_/' \
    deployments/docker/admin/.env.admin.example \
    deployments/docker/auth/.env.auth.example \
    deployments/docker/handler/.env.handler.example \
    deployments/docker/nginx/.env.nginx.example \
    > .env.local
```

- [https://localhost/auth_service/swagger/](https://localhost/auth_service/swagger/)

- [https://localhost/admin_service/swagger/](https://localhost/admin_service/swagger/)

- [https://localhost/handler_service/swagger/](https://localhost/handler_service/swagger/)

## Дополнительно

[Копирование данных из одной БД в другую](docx/dump_and_load_db.md)
