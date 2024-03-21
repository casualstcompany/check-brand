import json
from typing import Type

from models import BaseExtractLoadSchema
from transform.base_transformer import BaseTransformer


class ESTransformer(BaseTransformer):

    @staticmethod
    def actions_extend(actions, index, obj_id, obj_json):
        actions.extend(
            [
                json.dumps(
                    {
                        'index': {
                            '_index': index,
                            '_id': obj_id
                        }
                    }
                ),
                obj_json,
            ]
        )

    def transform(self, model: Type[BaseExtractLoadSchema], data):
        """Трансформирует из сырых данных Postgeres в документ(ы) ES"""

        index = model.get_class_meta().table
        actions = []

        if isinstance(data, list):

            for obj in data:
                obj = model(**dict(zip(model.get_field_names(), obj)))
                self.actions_extend(actions=actions, index=index, obj_id=obj.id, obj_json=obj.json())

        else:
            data = model(**dict(zip(model.get_field_names(), data)))
            self.actions_extend(actions=actions, index=index, obj_id=data.id, obj_json=data.json())

        return actions
