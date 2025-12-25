from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(
        load_only=True, required=True, validate=validate.Length(min=8)
    )


class UpdateUserSchema(Schema):
    username = fields.Str(validate=validate.Length(min=1, max=80))
    email = fields.Email(validate=validate.Length(max=120))


class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=1))
