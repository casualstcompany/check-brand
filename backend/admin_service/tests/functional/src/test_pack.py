from http import HTTPStatus

import pytest
from functional.config import TestUrls

urls = TestUrls()
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

@pytest.mark.asyncio
async def test_get_list_pack(make_get_request):
    response = await make_get_request(urls.pack, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status == HTTPStatus.OK
