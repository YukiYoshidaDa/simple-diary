from marshmallow import fields, validate

from extensions import ma


class RegisterSchema(ma.Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(required=True, validate=validate.Length(min=8))


class UpdateUserSchema(ma.Schema):
    username = fields.Str(validate=validate.Length(min=1, max=80))
    email = fields.Email(validate=validate.Length(max=120))
