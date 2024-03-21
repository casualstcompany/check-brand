# CheckBrand

### ЗАПУСК ПРОЕКТА

 При первом запуске необходимо создать сеть

~~~
 make dev_backend_create_network
~~~

И запустить полную загрузку сервисов

*Если на сервере разработки*
~~~
 make dev_backend_full_run
~~~

*Если на локальном компьютере*
~~~
 make local_backend_full_run
~~~
-----------------
### Импорт тестовых данных в БД трех сервисов (Auth, UGC, Admin)

 Необходимо запросить доступ к файлам на гугл диске

И произвести Импорт из этих файлов следующими командами

~~~
 docker exec -i AdminServiceDBDev /bin/bash -c "PGPASSWORD=example_password psql --username example_user example_db" < /home/CheckBrand/dump/admin_dump.sql
 docker exec -i AuthServiceDBDev /bin/bash -c "PGPASSWORD=password psql  --username admin auth_database" < /home/CheckBrand/dump/auth_dump.sql
 docker exec -i UGCServiceDBDev /bin/bash -c "PGPASSWORD=password psql --username admin ugc_database" < /home/CheckBrand/dump/ugc_dump.sql
~~~

Где путь */home/CheckBrand/dump/* заменить на свой локальный

#### Рекомендации по импорту данных
1. Каждую команду выполнить по несколько раз, так как с первого раза не все зависимости образуются
2. Команды запускать желательно с linux, на windows через wsl2
----------------
 ### До этого места документация верна))

----------------

----------------

----------------

----------------







git config --global core.autocrlf false

На данном этапе имеется три микросервиса
1) Admin - управление контентом
2) Auth - сервис автоизации
3) UGC - будет отвечать за взаимодействие пользователя с сервисом

Для разработки выделим порты:

AUTH = 50055, 5000, 5430

ADMIN = 8000, 5432

UGC = 6000, 5435

## РАЗРАБОТКА



Для корректной работы даже при разработке лучше обращаться к проекту через прокси сервер

[http://localhost](http://localhost) порт для разработки

*Доступные ссылки*

1. [http://localhost/admin_service/swagger/](http://localhost/admin_service/swagger/)
2. [http://localhost/admin_servicel/admin/](http://localhost/admin_service/admin/)

3. [http://localhost/ugc_service/api/openapi](http://localhost/ugc_service/api/openapi)

4. [http://localhost/auth_service/swagger/](http://localhost/auth_service/swagger/)

#### ADMIN SERVICE

Основные ссылки для обращения на прямую:
1. [http://localhost:8000/admin_service/swagger/](http://localhost:8000/admin_service/swagger/)
2. [http://localhost:8000/admin_service/admin/](http://localhost:8000/admin_service/admin/)

#### UGC SERVICE

Основные ссылки для обращения на прямую:
1. [http://localhost:6000/ugc_service/api_openapi/](http://localhost:8000/ugc_service/api_openapi/)


##TODO

1) Поменять версии в docker-compose (вроде на что то влияют они)


#docker-compose -f docker-compose.dev.yml run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d 1023951-cr24216.tmweb.ru
#docker-compose -f docker-compose.dev.yml run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d 1023951-cr24216.tmweb.ru


#docker-compose -f backend/ugc_service/docker-compose.dev.yml run service_dev alembic init models/migrations
#docker-compose -f backend/ugc_service/docker-compose.dev.yml run service_dev alembic revision --autogenerate -m "create inital tables"
#docker-compose -f backend/ugc_service/docker-compose.dev.yml run service_dev alembic upgrade head


docker container rm -f $(docker container ls -aq)
docker container prune

docker container rm -f $(docker container ls -aq)


docker image prune или docker image rm $(docker image ls -f dangling=true -q) или docker image rm $(docker image ls -q)

docker system df