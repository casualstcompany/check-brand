import json

from pydantic import ValidationError


def validation_model(model, data):
    try:
        return model(**data)
    except ValidationError:
        return False


async def decode_message(message):
    return json.loads(message.decode('utf-8'))
