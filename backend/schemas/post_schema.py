from marshmallow import fields, post_load, pre_load, validate

from models import Post

from .base import CTX_CURRENT_USER_ID, CTX_POST, BaseSchema


class PostSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    content = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    created_at = fields.DateTime()

    @pre_load
    def strip_content(self, data, **kwargs):
        if "content" in data and isinstance(data["content"], str):
            data["content"] = data["content"].strip()
        return data

    @post_load
    def make_post(self, data, **kwargs):
        # support updating an existing Post instance supplied via context
        existing: Post | None = self.context.get(CTX_POST)
        if existing:
            existing.content = data.get("content")
            return existing

        post = Post(content=data.get("content"))
        user_id = self.context.get(CTX_CURRENT_USER_ID)
        if user_id:
            post.user_id = user_id
        return post
