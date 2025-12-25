from marshmallow import Schema, fields, validate


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    content = fields.Str()
    created_at = fields.DateTime()


class PostCreateSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=500))


class PostUpdateSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=500))
