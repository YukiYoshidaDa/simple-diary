from flask import current_app
from marshmallow import ValidationError

from exceptions import ForbiddenError, NotFoundError, UnauthorizedError
from extensions import db
from models import User
from services.setting_service import create_default_settings


def register_user(validated_data: dict):
    """Create a new user from validated data (dict).

    Raises ValidationError for uniqueness violations. On DB errors, logs and re-raises.
    """
    username = validated_data.get("username")
    email = validated_data.get("email")
    password = validated_data.get("password")

    # uniqueness checks
    if User.query.filter_by(username=username).first():
        raise ValidationError({"username": ["Username already taken"]})
    if User.query.filter_by(email=email).first():
        raise ValidationError({"email": ["Email already registered"]})

    try:
        user = User(username=username, email=email)
        if password:
            user.set_password(password)
        db.session.add(user)
        db.session.flush()
        create_default_settings(user.id)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {e}")
        raise


def user_exists_by_username(username):
    return User.query.filter_by(username=username).first() is not None


def user_exists_by_email(email):
    return User.query.filter_by(email=email).first() is not None


def login_user(credentials: dict):
    """ログイン処理：失敗時は UnauthorizedError を投げる"""
    username = credentials.get("username")
    password = credentials.get("password")

    user = User.query.filter_by(username=username).first()

    # ユーザーが存在しない、またはパスワードが違う場合は例外を投げる
    if not user or not user.check_password(password):
        raise UnauthorizedError("Invalid username or password")

    return user


def get_all_users():
    """全ユーザーを取得"""
    return User.query.all()


def get_user_by_id(user_id):
    """IDでユーザーを取得"""
    return db.session.get(User, user_id)


def update_user_profile(user_id: int, validated_data: dict, current_user_id: int):
    """Update user identified by user_id using validated_data.

    Raises NotFoundError or ForbiddenError. Raises ValidationError for uniqueness.
    """
    # authorization: only the owner can update their profile
    if user_id != current_user_id:
        raise ForbiddenError("Not allowed to update this user")

    user = db.session.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")

    # uniqueness checks
    new_username = validated_data.get("username")
    new_email = validated_data.get("email")
    if new_username:
        existing = User.query.filter_by(username=new_username).first()
        if existing and existing.id != user_id:
            raise ValidationError({"username": ["Username already taken"]})
    if new_email:
        existing = User.query.filter_by(email=new_email).first()
        if existing and existing.id != user_id:
            raise ValidationError({"email": ["Email already registered"]})

    try:
        for attr in ("username", "email"):
            if attr in validated_data:
                setattr(user, attr, validated_data[attr])

        if "password" in validated_data and validated_data["password"]:
            user.set_password(validated_data["password"])

        db.session.commit()
        return user
    except Exception as e:
        current_app.logger.error(f"update_user_profile error: {e}")
        db.session.rollback()
        raise


def delete_user(user_id: int, current_user_id: int):
    """Delete user by id. Raises NotFoundError or ForbiddenError."""
    user = db.session.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")

    if user_id != current_user_id:
        raise ForbiddenError("Not allowed to delete this user")

    try:
        db.session.delete(user)
        db.session.commit()
        return True
    except Exception as e:
        current_app.logger.error(f"delete_user error: {e}")
        db.session.rollback()
        raise
