from pydoc import locate

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

from api.v1 import application
from core.config import get_settings as settings
from grpc_components import notification_grpc_client, admin_grpc_client

notification_grpc_client_cls = locate(settings.NOTIFICATION_GRPC.CLS)
admin_grpc_client_cls = locate(settings.ADMIN_GRPC.CLS)

app = FastAPI(
    title="UGC SERVICE API",
    version="1.0.0",
    description="Отвечает за все взаимодействия "
                "обычного пользователя с сервисом",
    docs_url=settings.BASE_URL + "/swagger",
    openapi_url=settings.BASE_URL + "/openapi.json",
    default_response_class=ORJSONResponse,
    redoc_url=None,
    debug=settings.DEBUG
)


@app.on_event('startup')
async def startup():
    notification_grpc_client.client = await notification_grpc_client_cls.create()
    admin_grpc_client.client = await admin_grpc_client_cls.create()
    # так же тут вызывать auth


@app.on_event('shutdown')
async def shutdown():
    await notification_grpc_client.client.close()
    await admin_grpc_client.client.close()
    # так же тут вызывать auth


@app.get(settings.BASE_URL + "/")
def read_root():
    # TODO: можно уже убрать(наверное)
    return {"Hello": "World"}


app.include_router(application.router, prefix=settings.BASE_URL + "/api/v1/applications")
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=6000, reload=True)
