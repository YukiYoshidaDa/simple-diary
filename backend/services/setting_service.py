from flask import current_app

from exceptions import ForbiddenError, NotFoundError
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
    settings = Setting.query.filter_by(user_id=user_id).first()
    if not settings:
        raise NotFoundError("Settings not found")
    return settings


def update_settings(user_id: int, validated_data: dict, current_user_id: int):
    """Update settings for user_id using validated_data.

    Raises NotFoundError or ForbiddenError. On DB errors, logs and re-raises.
    """
    if user_id != current_user_id:
        raise ForbiddenError("Not allowed to update settings for this user")

    settings = get_settings_by_user(user_id)
    if not settings:
        raise NotFoundError("Settings not found")

    try:
        for attr in ("theme", "notifications_enabled"):
            if attr in validated_data:
                setattr(settings, attr, validated_data[attr])

        db.session.commit()
        return settings
    except Exception as e:
        current_app.logger.error(f"update_settings error: {e}")
        db.session.rollback()
        raise
