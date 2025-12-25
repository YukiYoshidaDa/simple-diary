from typing import Any, Dict, Optional, Type, TypeVar

from marshmallow import Schema

SchemaT = TypeVar("SchemaT", bound=Schema)


# Standard context keys used across schemas
CTX_CURRENT_USER = "current_user"
CTX_CURRENT_USER_ID = "current_user_id"
CTX_POST = "post"


class BaseSchema(Schema):
    """Base Schema that centralizes context handling for Marshmallow 4.

    Marshmallow 4 removed passing context into `load(...)`. This BaseSchema
    accepts a `context` argument in its constructor and stores it on the
    instance as `self.context` so downstream hooks (`@pre_load`, `@post_load`,
    `@validates`) can access required runtime values.

    Usage:
      PostSchema(context={CTX_CURRENT_USER_ID: current_user.id}).load(data)

    The module also exposes a small factory helper `schema_with_context` to
    make call sites slightly more self-documenting.
    """

    def __init__(
        self, *args: Any, context: Optional[Dict[str, Any]] = None, **kwargs: Any
    ):
        # Keep an explicit dict on the instance for predictable access in hooks
        super().__init__(*args, **kwargs)
        self.context: Dict[str, Any] = dict(context or {})


def schema_with_context(schema_cls: Type[SchemaT], **context: Any) -> SchemaT:
    """Instantiate a Schema subclass with the provided context.

    This helper centralizes the `context=` call site and improves readability
    at the router layer.
    """

    return schema_cls(context=context)
