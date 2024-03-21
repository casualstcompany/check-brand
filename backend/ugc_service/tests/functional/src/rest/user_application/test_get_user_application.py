import logging
from http import HTTPStatus

import pytest

from functional.config import test_config as config
from functional.testdata import auth, collection


@pytest.mark.asyncio
async def test_get_by_collection_403(make_get_request):
    """Запрос без access токена"""

    response = await make_get_request(config.URLS.V1_APPLICATION_USER)

    assert response.status == HTTPStatus.FORBIDDEN
    assert response.body == auth.error_not_auth


@pytest.mark.asyncio
async def test_get_by_collection_404(make_get_request, get_access):
    """Использую левый collection_id"""

    response = await make_get_request(
        f"{config.URLS.V1_APPLICATION_USER}/6b93c655-243b-4096-ae7f-b7b30b13812c",
        headers={"Authorization": f"Bearer {await get_access}"}
    )

    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_by_collection_200(make_get_request, get_access):

    response = await make_get_request(
        f"{config.URLS.V1_APPLICATION_USER}/{collection.user_application.get('collection_id')}",
        headers={"Authorization": f"Bearer {await get_access}"}
    )

    assert response.status == HTTPStatus.OK
    assert response.body["id"] == collection.user_application.get('id')
    assert response.body["user_wallet"] == auth.login_data.get('public_address')


@pytest.mark.asyncio
async def test_get_by_collection_hide_404(make_get_request, get_access, caplog):
    """Данная заявка есть у пользователя, но она скрыта"""
    caplog.set_level(logging.INFO)

    response = await make_get_request(
        f"{config.URLS.V1_APPLICATION_USER}/{collection.user_application_hide.get('collection_id')}",
        headers={"Authorization": f"Bearer {await get_access}"}
    )

    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_by_collection_not_user_404(make_get_request, get_access, caplog):
    """Заявка активна, но не принадлежит пользователю"""
    caplog.set_level(logging.INFO)

    response = await make_get_request(
        f"{config.URLS.V1_APPLICATION_USER}/{collection.not_user_application.get('collection_id')}",
        headers={"Authorization": f"Bearer {await get_access}"}
    )

    assert response.status == HTTPStatus.NOT_FOUND
