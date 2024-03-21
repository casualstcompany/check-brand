IMAGE_FILE_EXTENSION = [
    "jpeg",
    "jpg",
    "png",
]
ICON_FILE_EXTENSION = [
    "svg",
    "png",
]
FILE_EXTENSION = [
    "jpg",
    "jpeg",
    "png",
    "mp4",
    "gif",
]


class Msg:
    error_check_royalty = (
        "The sum of investor_royalty and creator_royalty should be equal to"
        " percentage_fee collection"
    )
    error_check_currency_allowed_in_collection = (
        "The currency token is not listed as allowed in the collection"
    )
    error_blockchain_not_collection = (
        "The token blockchain does not match the collection blockchain"
    )
    error_account_not_collection_page = (
        "The selected account does not match the collection page"
    )
    error_amount_more_100_percent = "Amount cannot be more than 100 percent"
    error_collection_name_unique = (
        "The fields collection, name must make a unique set."
    )
    error_field_required = "This field is required."
    error_later_load = "Failed to load package. Try later."
    model_not_exist = "{model_name_str} with this id does not exist."
    collection_not_exist = "Collection with this id does not exist."
    pack_not_exist = "Pack with this id does not exist."
    blockchain_not_exist = "Blockchain with this id does not exist."
    page_not_exist = "Page with this id does not exist."
    random_number_not_integer = "Must be a integer."
    allowed_extension_image = (
        "File extension is not allowed. Allowed extensions are: jpeg, jpg,"
        " png."
    )
    allowed_extension_file = (
        "File extension is not allowed. Allowed extensions are: jpeg, jpg,"
        " png, mp4, gif."
    )
    does_not_match_the_existing_one = (
        "The specified value does not match the existing one."
    )
    data_editing_blocked = "Data editing is blocked."

    status_queue_broken = (
        "The status queue is broken. Status %s must be preceded by one of %s"
    )


msg = Msg()
