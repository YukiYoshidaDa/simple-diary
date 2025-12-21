from datetime import datetime

from models import db


class Post(db.Model):
    """ユーザーの投稿を管理するモデル"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """投稿情報を辞書型に変換"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Post {self.id} by User {self.user_id}>"
