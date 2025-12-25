from marshmallow import fields, post_load, pre_load, validate

from models import Setting

from .base import CTX_CURRENT_USER_ID, BaseSchema


class SettingSchema(BaseSchema):
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

    @post_load
    def make_setting(self, data, **kwargs):
        existing = self.context.get("settings")
        if existing:
            for k, v in data.items():
                setattr(existing, k, v)
            return existing
        # allow context to set user_id
        settings = Setting(**data)
        user_id = self.context.get(CTX_CURRENT_USER_ID)
        if user_id:
            settings.user_id = user_id
        return settings
