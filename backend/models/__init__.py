from extensions import db

from .post import Post  # noqa: E402, F401
from .setting import Setting  # noqa: E402, F401
from .user import User  # noqa: E402, F401

__all__ = ["db", "Post", "Setting", "User"]
