import pathlib
import random
import string
from io import BytesIO
from pathlib import Path
from typing import List
from uuid import UUID, uuid4

from django.core.files import File
from PIL import Image
from rest_framework import serializers
from rest_framework.utils import model_meta

from nft_tokens import constants
from nft_tokens.constants import msg


def get_list_by_field(validated_data: dict, field: str) -> list:
    # TODO описать функцию
    list_by_field = []
    if validated_data.get(field):
        list_by_field = validated_data.pop(field)

    if validated_data.get(field) == []:
        validated_data.pop(field)
    return list_by_field


def create_and_add_m2m(
    model, field, data, valid_exists=False, clear=False
) -> None:
    # TODO описать функцию
    if data and clear:
        field.clear()
    for item in data:
        if valid_exists:
            new_model = model.objects.filter(**item)
            if new_model.exists():
                new_model = new_model[0]
            else:
                new_model = model.objects.create(**item)
        else:
            new_model = model.objects.create(**item)

        field.add(new_model)


def check_sum_percent(data: dict, field: str) -> None:
    # TODO описать функцию
    if data.get(field):
        percent = 0

        for distribution in data.get(field):
            percent = percent + distribution.get("percent")

        if percent > 100:
            raise serializers.ValidationError(
                {field: [msg.error_amount_more_100_percent]}
            )


def set_if_value(mapping, key, value):
    if value:
        mapping[key] = value


def set_m2m_from_dict_to_instance(dict_m2m: dict, instance) -> None:
    info = model_meta.get_field_info(instance)
    m2m_fields = []
    for attr, value in dict_m2m.items():
        if attr in info.relations and info.relations[attr].to_many:
            m2m_fields.append((attr, value))

    for attr, value in m2m_fields:
        field = getattr(instance, attr)
        field.set(value)


def check_royalty(data: dict, instance=None) -> None:
    investor_royalty = data.get("investor_royalty")
    creator_royalty = data.get("creator_royalty")
    collection = data.get("collection")

    if instance:
        if investor_royalty is None:
            investor_royalty = instance.investor_royalty

        if creator_royalty is None:
            creator_royalty = instance.creator_royalty

        if not collection:
            collection = instance.collection

    if investor_royalty + creator_royalty != collection.percentage_fee:
        text = msg.error_check_royalty
        raise serializers.ValidationError(
            {"investor_royalty": [text], "creator_royalty": [text]},
        )


def check_currency_allowed_in_collection(data: dict, instance=None) -> None:
    collection = data.get("collection")
    if instance and not collection:
        collection = instance.collection
    currency = data.get("currency_token")
    if currency and currency not in collection.payment_tokens.all():
        raise serializers.ValidationError(
            {
                "currency_token": [
                    msg.error_check_currency_allowed_in_collection
                ]
            }
        )


def checking_dependency_two_fields(
    data, field_bool, field_main, instance=None
) -> None:
    # TODO описать функцию
    data_by_field_main = data.get(field_main)

    if instance and not data_by_field_main:
        data_by_field_main = getattr(instance, field_main)

    if data.get(field_bool) and not data_by_field_main:
        raise serializers.ValidationError(
            {f"{field_main}": [f"{field_main} field is required"]}
        )


def compress(file):
    extension = Path(file.name).suffix[1:].lower()
    if extension in constants.IMAGE_FILE_EXTENSION:
        im = Image.open(file)
        im_io = BytesIO()
        if extension == "png":
            im.save(im_io, "PNG", quality=60)
        else:
            im.save(im_io, "JPEG", quality=60)
        new_file = File(im_io, name=file.name)
    else:
        new_file = file

    return new_file


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True


def validate_int(number):
    if isinstance(number, int):
        return True
    return False


def validate_extension(file_name: str, allowed_extensions: List[str]):
    extension = pathlib.Path(file_name).suffix[1:].lower()
    if extension in allowed_extensions:
        return True
    return False


def file_generate_name_uuid(original_file_name, path=""):
    extension = pathlib.Path(original_file_name).suffix

    return f"{path}{uuid4().hex}{extension}"


def base_validate_create_update_pack_token(data, instance):
    """Метод используется для проверки при создании/обновление пака и токена"""

    checking_dependency_two_fields(data, "close", "close_image", instance)
    checking_dependency_two_fields(
        data, "unlockable", "unlockable_content", instance
    )

    check_currency_allowed_in_collection(data, instance)
    check_royalty(data, instance)

    check_sum_percent(data, "creator_royalty_distribution")
    check_sum_percent(data, "income_distribution")


def get_content_type_by_status_collection(status):
    content_type_by_status_collection = {
        "book": "booking_started",
        "mint_1": "minting_1_started",
        "mint_2": "minting_2_started",
        "sold_out": "sold_out",
    }
    return content_type_by_status_collection.get(status)


def random_name(length):
    letters = string.ascii_lowercase
    rand_string = "".join(random.choice(letters) for i in range(length))
    return rand_string


def random_number(length):
    letters = "1234567890"
    rand_string = "".join(random.choice(letters) for i in range(length))
    return rand_string
