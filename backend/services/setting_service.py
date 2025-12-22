from flask import current_app

from models import Setting, db


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

    for field in allowed_fields:
        if field in data and data[field] is not None:
            setattr(settings, field, data[field])

    db.session.commit()
    return settings
