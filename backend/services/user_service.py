from flask import current_app

from extensions import db
from models import User
from services.setting_service import create_default_settings


def register_user(user_obj):
    """ユーザーを登録（Schemaで作成された User インスタンスを受け取る）"""
    try:
        db.session.add(user_obj)
        db.session.flush()
        create_default_settings(user_obj.id)
        db.session.commit()
        return user_obj
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {e}")
        return None


def user_exists_by_username(username):
    return User.query.filter_by(username=username).first() is not None


def user_exists_by_email(email):
    return User.query.filter_by(email=email).first() is not None


def login_user(user_obj):
    """ログイン処理（LoginSchema が作った軽量オブジェクトを受け取る）"""
    username = getattr(user_obj, "username", None)
    password = getattr(user_obj, "password", None)
    user = User.query.filter_by(username=username).first()
    if user and password and user.check_password(password):
        return user
    return None


def get_all_users():
    """全ユーザーを取得"""
    return User.query.all()


def get_user_by_id(user_id):
    """IDでユーザーを取得"""
    return User.query.get(user_id)


def update_user_profile(user_obj):
    """更新済みの User インスタンスを受け取り、DB に永続化する"""
    try:
        # if detached instance with id, merge changes
        if not getattr(user_obj, "id", None):
            return None

        existing = User.query.get(user_obj.id)
        if not existing:
            return None

        # copy fields
        for attr in ("username", "email"):
            val = getattr(user_obj, attr, None)
            if val is not None:
                setattr(existing, attr, val)

        # password handled by schema (set_password on existing if provided)
        if getattr(user_obj, "password_hash", None) and not existing.password_hash:
            existing.password_hash = user_obj.password_hash

        db.session.commit()
        return existing
    except Exception as e:
        current_app.logger.error(f"update_user_profile error: {e}")
        db.session.rollback()
        return None


def delete_user(user_id):
    """ユーザーを削除"""
    try:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    except Exception as e:
        current_app.logger.error(f"delete_user error: {e}")
        db.session.rollback()
        return False
