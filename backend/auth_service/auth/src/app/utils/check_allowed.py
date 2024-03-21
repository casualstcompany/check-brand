from uuid import UUID

ALLOWED_EXTENSIONS_IMAGES = {"png", "jpg", "jpeg"}


def check_image_to_allowed(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGES
    )


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True
