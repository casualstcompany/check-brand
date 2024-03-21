from fastapi import APIRouter

from api.v1.application import application, tokens, users

router = APIRouter(prefix="")
router.include_router(users.router, prefix="/users",)
router.include_router(tokens.router, prefix="/tokens",)
router.include_router(application.router)
