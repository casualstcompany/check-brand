from marshmallow import Schema, fields


class GetNonceSchema(Schema):
    public_address = fields.String(required=True)


class AuthenticationSchema(Schema):
    public_address = fields.String(required=True)
    signature = fields.String(required=True)
