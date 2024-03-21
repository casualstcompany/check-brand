from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api import constant
from models import PackDetail, PackList, PackListPage
from models.filter import PackFilter
from services.packs import PackService, get_pack_service


router = APIRouter()


@router.get("/{pack_id}", response_model=PackDetail,
            summary="Пакет по его id",
            description="Вся информация о пакетах",
            tags=["Pack"]
            )
async def pack_detail(pack_id: UUID, pack_service: PackService = Depends(get_pack_service)) -> PackDetail:

    pack = await pack_service.get_by_id(str(pack_id))

    if not pack:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.PACK_NOT_FOUND)

    return PackDetail.parse_obj(pack)


@router.get("/", response_model=PackListPage,
            summary="Список пакетов",
            response_description="В списках пока вся информация о пакетах.",
            tags=['Pack']
            )
async def pack_list(query_model: PackFilter = Depends(PackFilter),
                    pack_service: PackService = Depends(get_pack_service)) -> PackListPage:

    packs, count, total_pages = await pack_service.get_specific_data(query_model)

    return PackListPage(
        results=[PackList.parse_obj(pack) for pack in packs],
        count=count,
        total_pages=total_pages,
        page=query_model.page,
        page_size=query_model.page_size
    )
