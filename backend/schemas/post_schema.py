from marshmallow import fields, validate

from extensions import ma


class PostCreateSchema(ma.Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=500))


class PostUpdateSchema(ma.Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=500))
