from extensions import db


class Setting(db.Model):
    """
    ユーザーの個人設定（通知・外観）を管理するモデル
    """

    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    notifications_enabled = db.Column(db.Boolean, default=True)
    theme = db.Column(db.String(20), default="light")

    def to_dict(self):
        """設定情報を辞書型に変換"""
        return {
            "user_id": self.user_id,
            "theme": self.theme,
            "notifications_enabled": self.notifications_enabled,
        }

    def __repr__(self):
        return f"<Setting user_id={self.user_id} theme='{self.theme}'>"
