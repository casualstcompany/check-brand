## API  сервис

Составляющая Handler Service, Позволяет пользователю взаимодействовать с сервисом.

## Запуск Микросервиса
```commandline
docker-compose -f docker-compose.dev.yml --env-file handler.example.env  up --build
```

Сейчас пробил временно директорию на компе в контейнер, теперь при сохранении не надо перезапускать.

#### *Для удобства, команда в отдельном терминале запускает только сервис*
```commandline
docker-compose -f docker-compose.dev.yml --env-file handler.example.env  up --build api_service
```