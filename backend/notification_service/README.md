Сервис уведомлений 
==================


## Ссылки

[ADMIN PANEL Notification локальная ](http://localhost/notification_service/admin/)

!!!!!!!!!!!!!!!!!!!!!иногда не отлавливает 400 при отправке на smtp


*Генерация кода для GRPC из PROTO*
```
python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/components/grpc/protobufs/notification_api.proto
```

*TEST Генерация кода для GRPC из PROTO*
```
python -m grpc_tools.protoc -I ../tests --python_out=. --grpc_python_out=. ../tests/functional/protobufs/notification_api.proto
```

*TEST Генерация кода для GRPC из PROTO*
```
python -m grpc_tools.protoc -I ../src --python_out=. --grpc_python_out=. ../src/components/protobufs/notification.proto
```

#python manage.py generateproto её необходимо использовать при разработке

{
"collection_name": "Reebok NFT Certificates",
"collection_image_url": "https://zwkhyf.stripocdn.email/content/guids/CABINET_76322d2a10f10798f805d3fac093f16d3b86142f61a3141dd8dfb9a9dff03d6c/images/r1.jpg"
}

{
"collection_name": "Test",
"collection_image_url": ""
}

## Варианты писем и их payload

1. ### added_white_list

*Должен отправить сервер запрашивающий уведомление*
```
{
"email": ["test@mail.ru", ],
"collection_id": "UUID",
"user_wallet": "0xsasadasdasdasd",
"collection_name": "Reebok NFT Certificates",
"collection_image_url": "https://zwkhyf.stripocdn.email/content/guids/CABINET_76322d2a10f10798f805d3fac093f16d3b86142f61a3141dd8dfb9a9dff03d6c/images/r1.jpg"
}
```

*Служит в качестве проверки в админке*
```
{
"collection_name": "Reebok NFT Certificates",
"collection_image_url": "https://zwkhyf.stripocdn.email/content/guids/CABINET_76322d2a10f10798f805d3fac093f16d3b86142f61a3141dd8dfb9a9dff03d6c/images/r1.jpg"
}
```

2. ### booking_started
4. ### minting_1_started
6. ### minting_2_started
8. ### sold_out

*Должен отправить сервер запрашивающий уведомление*
```
{
"email": ["test@mail.ru", ],
"collection_id": "UUID",
"collection_name": "Reebok NFT Certificates",
"collection_image_url": "https://zwkhyf.stripocdn.email/content/guids/CABINET_76322d2a10f10798f805d3fac093f16d3b86142f61a3141dd8dfb9a9dff03d6c/images/r1.jpg"
}
```

*Служит в качестве проверки в админке*
```
{
"collection_name": "Reebok NFT Certificates",
"collection_image_url": "https://zwkhyf.stripocdn.email/content/guids/CABINET_76322d2a10f10798f805d3fac093f16d3b86142f61a3141dd8dfb9a9dff03d6c/images/r1.jpg"
}
```

3. ### added_white_list_and_booking
5. ### added_white_and_expects
7. ### added_white_list_and_minting_2

*Должен отправить сервер запрашивающий уведомление*
```
{
"email": ["test@mail.ru", ],
"collection_id": "UUID",
"user_wallet": "0xsasadasdasdasd",
"collection_name": "Reebok NFT Certificates",
"collection_image_url": "https://zwkhyf.stripocdn.email/content/guids/CABINET_76322d2a10f10798f805d3fac093f16d3b86142f61a3141dd8dfb9a9dff03d6c/images/r1.jpg"
}
```

*Служит в качестве проверки в админке*
```
{
"collection_name": "Reebok NFT Certificates",
"collection_image_url": "https://zwkhyf.stripocdn.email/content/guids/CABINET_76322d2a10f10798f805d3fac093f16d3b86142f61a3141dd8dfb9a9dff03d6c/images/r1.jpg"
}
```
9. ### user_booked

[//]: # TODO: сейчас  url у токена кривой, подставляется только id()
*Должен отправить сервер запрашивающий уведомления.*
```
{
    "email": ["test@mail.ru", ],
    "collection_id": "UUID",
    "user_wallet": "0xsasadasdasdasd",
    "token_id": "UUID",
    "token_name": "str",
    "token_file_url": "str",
    "collection_name": "Reebok NFT Certificates",
    "collection_image_url": "https://zwkhyf.stripocdn.email/content/guids/CABINET_76322d2a10f10798f805d3fac093f16d3b86142f61a3141dd8dfb9a9dff03d6c/images/r1.jpg"
}

```

*Служит в качестве проверки в админке*
```
{
    "token_id": "UUID",
    "token_name": "Unique CARD TEST",
    "collection_name": "Reebok NFT Certificates",
    "token_file_url": "https://zwkhyf.stripocdn.email/content/guids/CABINET_76322d2a10f10798f805d3fac093f16d3b86142f61a3141dd8dfb9a9dff03d6c/images/r1.jpg"
}
```
