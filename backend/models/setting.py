from models import db


class Setting(db.Model):
    """ユーザーの設定を管理するモデル"""

    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    notifications_enabled = db.Column(db.Boolean, default=True)  # 通知の有効/無効
    language = db.Column(db.String(50), default="jp")  # 言語設定
