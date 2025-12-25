from marshmallow import Schema, fields, validate


class SettingSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    theme = fields.Str()
    notifications_enabled = fields.Boolean()


class SettingUpdateSchema(Schema):
    theme = fields.Str(validate=validate.OneOf(["light", "dark"]))
    notifications_enabled = fields.Boolean()
