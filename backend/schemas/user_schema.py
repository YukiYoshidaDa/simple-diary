from marshmallow import Schema, fields, pre_load, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(
        load_only=True, required=True, validate=validate.Length(min=8)
    )

    @pre_load
    def strip_strings(self, data, **kwargs):
        for k in ("username", "email", "password"):
            if k in data and isinstance(data[k], str):
                data[k] = data[k].strip()
        return data


class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=1))

    @pre_load
    def strip_strings(self, data, **kwargs):
        for k in ("username", "password"):
            if k in data and isinstance(data[k], str):
                data[k] = data[k].strip()
        return data
