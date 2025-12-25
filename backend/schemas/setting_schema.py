from marshmallow import fields, validate

from extensions import ma


class SettingUpdateSchema(ma.Schema):
    theme = fields.Str(validate=validate.OneOf(["light", "dark"]))
    notifications_enabled = fields.Boolean()
