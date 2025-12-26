import pytest
from marshmallow import ValidationError
from services import user_service
from models import User


def test_register_user_success(db):
    """ユーザー登録が正常に動作することを確認"""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword",
    }
    user = user_service.register_user(data)

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    # DBに保存されているか確認
    assert User.query.filter_by(username="testuser").first() is not None


def test_register_user_duplicate_username(db):
    """既存のユーザー名での登録が失敗することを確認"""
    data = {"username": "dupuser", "email": "user1@example.com", "password": "password"}
    user_service.register_user(data)

    # 2回目（同じユーザー名）
    data2 = {
        "username": "dupuser",
        "email": "user2@example.com",
        "password": "password",
    }
    with pytest.raises(ValidationError) as excinfo:
        user_service.register_user(data2)

    assert "Username already taken" in str(excinfo.value)


def test_register_user_duplicate_email(db):
    """既存のメールアドレスでの登録が失敗することを確認"""
    data = {"username": "user1", "email": "dup@example.com", "password": "password"}
    user_service.register_user(data)

    # 2回目（同じメールアドレス）
    data2 = {"username": "user2", "email": "dup@example.com", "password": "password"}
    with pytest.raises(ValidationError) as excinfo:
        user_service.register_user(data2)

    assert "Email already registered" in str(excinfo.value)


def test_login_user_success(db):
    """正しい認証情報でログインできることを確認"""
    data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "correctpassword",
    }
    user_service.register_user(data)

    credentials = {"username": "loginuser", "password": "correctpassword"}
    user = user_service.login_user(credentials)
    assert user.username == "loginuser"


def test_login_user_invalid_password(db):
    """間違ったパスワードでログインに失敗することを確認"""
    from exceptions import UnauthorizedError

    data = {
        "username": "loginuser",
        "email": "token@example.com",
        "password": "correctpassword",
    }
    user_service.register_user(data)

    credentials = {"username": "loginuser", "password": "wrongpassword"}
    with pytest.raises(UnauthorizedError):
        user_service.login_user(credentials)
