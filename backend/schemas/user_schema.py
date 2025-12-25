from marshmallow import (
    ValidationError,
    fields,
    post_load,
    pre_load,
    validate,
    validates,
)

from models import User

from .base import CTX_CURRENT_USER, CTX_CURRENT_USER_ID, BaseSchema


class UserSchema(BaseSchema):
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

    @validates("username")
    def validate_username(self, value, **kwargs):
        current_user_id = self.context.get(CTX_CURRENT_USER_ID)
        existing = User.query.filter_by(username=value).first()
        if existing and (current_user_id is None or existing.id != current_user_id):
            raise ValidationError("Username already taken")

    @validates("email")
    def validate_email(self, value, **kwargs):
        current_user_id = self.context.get(CTX_CURRENT_USER_ID)
        existing = User.query.filter_by(email=value).first()
        if existing and (current_user_id is None or existing.id != current_user_id):
            raise ValidationError("Email already registered")

    @post_load
    def make_user(self, data, **kwargs):
        # If context provides an existing instance, update it
        existing = self.context.get(CTX_CURRENT_USER)
        if existing:
            for k, v in data.items():
                if k == "password":
                    existing.set_password(v)
                else:
                    setattr(existing, k, v)
            return existing

        # Create new User instance
        user = User(username=data.get("username"), email=data.get("email"))
        if data.get("password"):
            user.set_password(data.get("password"))
        return user


class LoginSchema(BaseSchema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=1))

    @pre_load
    def strip_strings(self, data, **kwargs):
        for k in ("username", "password"):
            if k in data and isinstance(data[k], str):
                data[k] = data[k].strip()
        return data

    @post_load
    def make_user(self, data, **kwargs):
        # Return a lightweight object for authentication use
        from types import SimpleNamespace

        return SimpleNamespace(
            username=data.get("username"), password=data.get("password")
        )
