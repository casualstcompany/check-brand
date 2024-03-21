import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseSchema(BaseModel):

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        orm_mode = True

    class Meta:
        pass

    @classmethod
    def get_class_meta(cls):
        return cls.Meta


class BaseComponentExtractLoadSchema(BaseSchema):

    class Meta:
        array_agg = None
        left_join = None


class BaseExtractLoadSchema(BaseSchema):
    id: str

    class Meta:
        schema = None
        table = None
        field_group_by = None
        state_key_update_at = None

    @classmethod
    def get_list_names_simple_fields(cls):
        return [cls.get_class_meta().table + "." + field_name for field_name in cls.__fields__.keys() if
                not issubclass(cls.__fields__.get(field_name).type_, BaseComponentExtractLoadSchema) and field_name != "updated_at"]

    @classmethod
    def get_field_names(cls):
        return [field_name for field_name in cls.__fields__.keys()]

    @classmethod
    def get_names_complex_fields(cls):
        return [field_name for field_name in cls.__fields__.keys() if
                issubclass(cls.__fields__.get(field_name).type_, BaseComponentExtractLoadSchema)]

    @classmethod
    def get_greatest(cls, not_max: bool = False):
        greatest = "GREATEST(%s.updated_at" % cls.Meta.table
        for field_name in cls.__fields__.keys():
            if issubclass(cls.__fields__.get(field_name).type_, BaseComponentExtractLoadSchema):
                if not_max:
                    greatest += ", %s_%s.updated_at" % (field_name, cls.Meta.table)
                else:
                    greatest += ", MAX(%s_%s.updated_at)" % (field_name, cls.Meta.table)
        greatest += ")"
        return greatest

    @classmethod
    def get_list_complex_fields_meta_array_agg(cls):
        return [
            cls.__fields__.get(field_name).type_.get_class_meta().array_agg
            for field_name in cls.__fields__.keys()
            if issubclass(cls.__fields__.get(field_name).type_, BaseComponentExtractLoadSchema)
        ]

    @classmethod
    def get_list_complex_fields_meta_left_join(cls):
        return [
            cls.__fields__.get(field_name).type_.get_class_meta().left_join
            for field_name in cls.__fields__.keys()
            if issubclass(cls.__fields__.get(field_name).type_, BaseComponentExtractLoadSchema)
        ]
