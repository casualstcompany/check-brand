from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api import constant
from models import PageDetail, PageList, PageListPage
from models.filter import PageFilter
from services.pages import PageService, get_page_service


router = APIRouter()


@router.get("/{page_id}", response_model=PageDetail,
            summary="Страница по ее id",
            description="Вся информация о странице",
            tags=["Page"]
            )
async def page_detail(page_id: UUID, page_service: PageService = Depends(get_page_service)) -> PageDetail:

    page = await page_service.get_by_id(str(page_id))

    if not page:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.PAGE_NOT_FOUND)

    return PageDetail.parse_obj(page)


@router.get("/", response_model=PageListPage,
            summary="Список страниц",
            response_description="В списках пока вся информация о страницах.",
            tags=['Page']
            )
async def page_list(query_model: PageFilter = Depends(PageFilter),
                    page_service: PageService = Depends(get_page_service)) -> PageListPage:

    pages, count, total_pages = await page_service.get_specific_data(query_model)

    return PageListPage(
        results=[PageList.parse_obj(page) for page in pages],
        count=count,
        total_pages=total_pages,
        page=query_model.page,
        page_size=query_model.page_size
    )
