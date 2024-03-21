from http import HTTPStatus

from uuid import UUID


from fastapi import APIRouter, Depends, HTTPException


from api import constant
from models import CollectionDetail, CollectionList, CollectionListPage, CollectionSimpleList, \
    CollectionSimpleListPage, CollectionListRankingsPage, CollectionListRankings
from models.filter import CollectionFilter, CollectionRankingsFilter
from services.collections import CollectionService, get_collection_service


router = APIRouter()


@router.get("/{collection_id}", response_model=CollectionDetail,
            summary="Коллекция по его id",
            description="Вся информация о коллекциях",
            tags=["Collection"]
            )
async def collection_detail(collection_id: UUID,
                            collection_service: CollectionService = Depends(get_collection_service)
                            ) -> CollectionDetail:
    collection = await collection_service.get_by_id(str(collection_id))

    if not collection:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.COLLECTION_NOT_FOUND)

    return CollectionDetail.parse_obj(collection)


@router.get("/", response_model=CollectionListPage,
            summary="Список коллекций",
            response_description="В списках пока вся информация о коллекциях.",
            tags=['Collection']
            )
async def collection_list(query_model: CollectionFilter = Depends(CollectionFilter),
                          collection_service: CollectionService = Depends(get_collection_service)
                          ) -> CollectionListPage:
    collections, count, total_pages = await collection_service.get_specific_data(query_model)

    return CollectionListPage(
        results=[CollectionList.parse_obj(collection) for collection in collections],
        count=count,
        total_pages=total_pages,
        page=query_model.page,
        page_size=query_model.page_size
    )


@router.get("/rankings/", response_model=CollectionListRankingsPage,
            summary="Список коллекций для страницы Rankings",
            response_description="В списках необходимая информация о коллекциях.",
            tags=['Collection']
            )
async def collection_list_rankings(query_model: CollectionRankingsFilter = Depends(CollectionRankingsFilter),
                                   collection_service: CollectionService = Depends(get_collection_service)
                                   ) -> CollectionListRankingsPage:
    collections, count, total_pages = await collection_service.get_specific_data(query_model)

    return CollectionListRankingsPage(
        results=[CollectionListRankings.parse_obj(collection) for collection in collections],
        count=count,
        total_pages=total_pages,
        page=query_model.page,
        page_size=query_model.page_size
    )


@router.get("/simplified/", response_model=CollectionSimpleListPage,
            summary="Список коллекций с минимальным набором данных",
            response_description="В списках минимум информации о коллекциях.",
            tags=['Collection']
            )
async def collection_simple_list(query_model: CollectionFilter = Depends(CollectionFilter),
                                 collection_service: CollectionService = Depends(get_collection_service)
                                 ) -> CollectionSimpleListPage:
    collections, count, total_pages = await collection_service.get_specific_data(query_model)

    results = [
        CollectionSimpleList(
            id=collection.id, name=collection.name,
            logo=collection.logo, account_id=collection.account.id
        ) for collection in collections
    ]

    return CollectionSimpleListPage(
        results=results,
        count=count,
        total_pages=total_pages,
        page=query_model.page,
        page_size=query_model.page_size
    )
