from flask import current_app

from models import User, db
from services.setting_service import create_default_settings


def register_user(username, email, password):
    """ユーザーを登録"""
    if (
        User.query.filter_by(username=username).first()
        or User.query.filter_by(email=email).first()
    ):
        return None  # ユーザーが既に存在する場合は None を返す
    try:
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # パスワードをハッシュ化して保存
        db.session.add(new_user)
        db.session.flush()
        create_default_settings(new_user.id)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {e}")
        return None


def login_user(username, password):
    """ログイン処理"""
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None


def get_all_users():
    """全ユーザーを取得"""
    return User.query.all()


def get_user_by_id(user_id):
    """IDでユーザーを取得"""
    return User.query.get(user_id)


def update_user_profile(user_id, data):
    """ユーザー情報を更新"""
    user = User.query.get(user_id)
    if not user:
        return None

    allowed_fields = {"username", "email"}

    for field in allowed_fields:
        if field in data and data[field] is not None:
            setattr(user, field, data[field])

    db.session.commit()
    return user


def delete_user(user_id):
    """ユーザーを削除"""
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
