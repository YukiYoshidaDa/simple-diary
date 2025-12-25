from marshmallow import Schema, fields, pre_load, validate


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    content = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    created_at = fields.DateTime()

    @pre_load
    def strip_content(self, data, **kwargs):
        if "content" in data and isinstance(data["content"], str):
            data["content"] = data["content"].strip()
        return data
