from fastapi import APIRouter

from . import tokens, packs, collections, accounts, pages


router = APIRouter(prefix="")
router.include_router(tokens.router, prefix="/token")
router.include_router(packs.router, prefix="/pack")
router.include_router(collections.router, prefix="/collection")
router.include_router(accounts.router, prefix="/account")
router.include_router(pages.router, prefix="/page")
