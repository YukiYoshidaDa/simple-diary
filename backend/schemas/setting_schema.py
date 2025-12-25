from marshmallow import Schema, fields, pre_load, validate


class SettingSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    theme = fields.Str(validate=validate.OneOf(["light", "dark"]))
    notifications_enabled = fields.Boolean()

    @pre_load
    def normalize(self, data, **kwargs):
        if "theme" in data and isinstance(data["theme"], str):
            data["theme"] = data["theme"].strip()
        # normalize boolean-like values
        if "notifications_enabled" in data:
            val = data["notifications_enabled"]
            if isinstance(val, str):
                data["notifications_enabled"] = val.lower() in ("1", "true", "yes")
        return data
