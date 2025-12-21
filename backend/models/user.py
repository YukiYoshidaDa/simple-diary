from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from models import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def set_password(self, password):
        """パスワードをハッシュ化して保存"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """入力されたパスワードとハッシュを比較"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        """ユーザー情報を辞書型に変換"""
        return {"id": self.id, "username": self.username, "email": self.email}

    def __repr__(self):
        return f"<User {self.username}>"
