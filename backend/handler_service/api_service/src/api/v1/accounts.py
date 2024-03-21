from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api import constant
from models import AccountDetail, AccountSimpleList, AccountSimpleListPage, AccountList, AccountListPage
from models.filter import AccountFilter
from services.accounts import AccountService, get_account_service


router = APIRouter()


@router.get("/{account_id}", response_model=AccountDetail,
            summary="Аккаунт по его id",
            description="Вся информация об аккаунте",
            tags=["Account"]
            )
async def account_detail(
        account_id: UUID,
        account_service: AccountService = Depends(get_account_service)) -> AccountDetail:

    account = await account_service.get_by_id(str(account_id))

    if not account:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.ACCOUNT_NOT_FOUND)

    return AccountDetail.parse_obj(account)


@router.get("/", response_model=AccountListPage,
            summary="Список аккаунтов",
            response_description="В списках пока вся информация об аккаунтах.",
            tags=['Account']
            )
async def account_list(query_model: AccountFilter = Depends(AccountFilter),
                       account_service: AccountService = Depends(get_account_service)) -> AccountListPage:

    accounts, count, total_pages = await account_service.get_specific_data(query_model)

    return AccountListPage(
        results=[AccountList.parse_obj(account) for account in accounts],
        count=count,
        total_pages=total_pages,
        page=query_model.page,
        page_size=query_model.page_size
    )


@router.get("/simplified/", response_model=AccountSimpleListPage,
            summary="Список аккаунтов с минимальным набором данных",
            response_description="В списках минимум информации об аккаунтах.",
            tags=['Account']
            )
async def account_simple_list(query_model: AccountFilter = Depends(AccountFilter),
                              account_service: AccountService = Depends(get_account_service)) -> AccountSimpleListPage:

    accounts, count, total_pages = await account_service.get_specific_data(query_model)

    return AccountSimpleListPage(
        results=[AccountSimpleList.parse_obj(account) for account in accounts],
        count=count,
        total_pages=total_pages,
        page=query_model.page,
        page_size=query_model.page_size
    )
