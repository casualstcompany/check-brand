from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api import constant
from core.utils import get_price_in_usd
from models import TokenDetail, TokenList
from models.filter import TokenFilter
from models.token import TokenListPage
from services.tokens import TokenService, get_token_service


router = APIRouter()


@router.get("/{token_id}", response_model=TokenDetail,
            summary="Токен по его id",
            description="Вся информация о тюкине",
            tags=["Token"]
            )
async def token_detail(token_id: UUID, token_service: TokenService = Depends(get_token_service)) -> TokenDetail:

    token = await token_service.get_by_id(str(token_id))

    if not token:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.TOKEN_NOT_FOUND)

    obj = TokenDetail.parse_obj(token)
    obj.price_in_usd = await get_price_in_usd(price=obj.price)

    return obj


@router.get("/", response_model=TokenListPage,
            summary="Список токенов",
            response_description="В списках пока вся информация о токенах.",
            tags=['Token']
            )
async def token_list(query_model: TokenFilter = Depends(TokenFilter),
                     token_service: TokenService = Depends(get_token_service)) -> TokenListPage:

    tokens, count, total_pages = await token_service.get_specific_data(query_model)

    return TokenListPage(
        results=[TokenList.parse_obj(token) for token in tokens],
        count=count,
        total_pages=total_pages,
        page=query_model.page,
        page_size=query_model.page_size
    )
