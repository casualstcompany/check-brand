import logging
import uuid

import grpc
from google.protobuf.struct_pb2 import Struct
import pytest

from functional.protobufs.notification_api_pb2 import NotificationRequest


@pytest.mark.asyncio
async def test_notify_user(get_notification_client, caplog):
    caplog.set_level(logging.INFO)

    client = get_notification_client

    payload = Struct()
    payload.update({
        "collection_name": "Reebok NFT(TEST) Certificates",
"collection_image_url": "https://zwkhyf.stripocdn.email/content/guids/CABINET_76322d2a10f10798f805d3fac093f16d3b86142f61a3141dd8dfb9a9dff03d6c/images/r1.jpg",
        "email": ["dry.wats@gmail.com", "mwtech@mail.ru"]
    })

    request = NotificationRequest(id=str(uuid.uuid4()),
                                  content_type="added_white_list",
                                  payload=payload
                                  )

    response = client.NotifyUser(request)

    assert response.status == "success"


@pytest.mark.asyncio
async def test_notify_user_error(get_notification_client, caplog):
    caplog.set_level(logging.INFO)

    client = get_notification_client

    payload = Struct()
    payload.update({
        "content": "hello world",
        "email": ["dry.wats@gmail.com"]
    })

    request = NotificationRequest(content_type="test",
                                  payload=payload)

    try:
        response = client.NotifyUser(request)
    except grpc.RpcError as e:
        status_code = e.code()
        assert status_code == grpc.StatusCode.INVALID_ARGUMENT


@pytest.mark.asyncio
async def test_notify_user_bad_id(get_notification_client, caplog):
    caplog.set_level(logging.INFO)

    client = get_notification_client
    payload = Struct()
    payload.update({
        "content": "hello world",
        "email": ["dry.wats@gmail.com"]
    })
    request = NotificationRequest(id="sas", payload=payload)
    try:
        response = client.NotifyUser(request)
    except grpc.RpcError as e:
        status_code = e.code()

    assert status_code == grpc.StatusCode.INVALID_ARGUMENT
