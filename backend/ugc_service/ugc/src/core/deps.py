from fastapi import Depends

from core import error
from core.auth import JWTBearer
from core.config import get_settings as settings
from db.postgres import async_session
from schemas.auth import User


async def get_async_db():
    async with async_session() as db:
        yield db


class ContextManagerAsyncSession:
    def __init__(self):
        self.db = async_session()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_current_user(user: dict = Depends(JWTBearer())) -> User:
    return User(user_wallet=user["user_wallet"], user_role=user["user_role"])


async def get_moderator(user: User = Depends(get_current_user)):
    for role in settings.ALLOWED_ROLES_FOR_MODERATOR:
        if role in user.user_role:
            return user
    raise error.BaseError(status_code=403, detail="no access rights")
