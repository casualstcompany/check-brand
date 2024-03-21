from uuid import UUID

from pydantic import ValidationError

from core import error


async def none_or_not_found(obj):
    if obj is None:
        raise error.BaseError(status_code=404, detail="Not Found")


async def validation_schema(schema, data):
    try:
        return schema(**data)
    except ValidationError as e:
        raise error.BaseError(status_code=422, detail=e.errors())


async def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True


async def get_content_type_by_status_collection(status):
    # TODO: разобраться если смысл функции такого типа делать асинхронными
    content_type_by_status_collection = {
        "stop": "added_white_list",
        "book": "added_white_list_and_booking",
        "mint_1": "added_white_and_expects",
        "mint_2": "added_white_list_and_minting_2",
    }
    return content_type_by_status_collection.get(status)


def get_content_type_by_status_collection_sync(status):
    content_type_by_status_collection = {
        "stop": "added_white_list",
        "book": "added_white_list_and_booking",
        "mint_1": "added_white_and_expects",
        "mint_2": "added_white_list_and_minting_2",
    }
    return content_type_by_status_collection.get(status)
