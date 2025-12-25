from flask import current_app

from extensions import db
from models import Setting


def create_default_settings(user_id):
    """新規ユーザー用の初期設定を作成する"""
    new_settings = Setting(
        user_id=user_id,
        theme=current_app.config.get("DEFAULT_THEME", "light"),
        notifications_enabled=current_app.config.get(
            "DEFAULT_NOTIFICATIONS_ENABLED", True
        ),
    )
    db.session.add(new_settings)
    return new_settings


def get_settings_by_user(user_id):
    """特定のユーザーの設定を取得する"""
    return Setting.query.filter_by(user_id=user_id).first()


def update_settings(settings_obj):
    """Schema で生成・更新された Setting インスタンスを受け取り永続化する"""
    try:
        # ensure we have user_id to find existing
        user_id = getattr(settings_obj, "user_id", None)
        if not user_id:
            return None

        settings = get_settings_by_user(user_id)
        if not settings:
            return None

        for attr in ("theme", "notifications_enabled"):
            val = getattr(settings_obj, attr, None)
            if val is not None:
                setattr(settings, attr, val)

        db.session.commit()
        return settings
    except Exception as e:
        current_app.logger.error(f"update_settings error: {e}")
        db.session.rollback()
        return None
