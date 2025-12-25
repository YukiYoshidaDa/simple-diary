from flask import current_app

from extensions import db
from models import Setting


def create_default_settings(user_id):
    """新規ユーザー用の初期設定を作成する"""
    new_settings = Setting(
        user_id=user_id, theme=current_app.config.get("DEFAULT_THEME", "light")
    )
    db.session.add(new_settings)
    return new_settings


def get_settings_by_user(user_id):
    """特定のユーザーの設定を取得する"""
    return Setting.query.filter_by(user_id=user_id).first()


def update_settings(user_id, data):
    settings = get_settings_by_user(user_id)
    if not settings:
        return None
    allowed_fields = {"theme", "notifications_enabled"}

    try:
        for field in allowed_fields:
            if field in data and data[field] is not None:
                # notifications_enabled は真偽値に正規化
                if field == "notifications_enabled":
                    val = data[field]
                    if isinstance(val, str):
                        val = val.lower() in ("1", "true", "yes")
                    setattr(settings, field, bool(val))
                else:
                    setattr(settings, field, data[field])

        db.session.commit()
        return settings
    except Exception as e:
        current_app.logger.error(f"update_settings error: {e}")
        db.session.rollback()
        return None
