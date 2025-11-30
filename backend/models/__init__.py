from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

from .user import User  # noqa: E402, F401
from .setting import Setting  # noqa: E402, F401
from .post import Post  # noqa: E402, F401
