import pytest
from marshmallow import ValidationError

from schemas.post_schema import PostSchema
from schemas.setting_schema import SettingSchema
from schemas.user_schema import UserSchema


def test_user_schema_load_success():
    data = {"username": "testuser", "email": "test@example.com", "password": "password"}
    result = UserSchema().load(data)
    assert result["username"] == "testuser"
    assert "password" in result


def test_user_schema_load_invalid_email():
    data = {"username": "testuser", "email": "not-an-email", "password": "password123"}
    with pytest.raises(ValidationError) as excinfo:
        UserSchema().load(data)
    assert "email" in excinfo.value.messages


def test_user_schema_username_boundary():
    # max 80 characters
    long_username = "a" * 81
    data = {
        "username": long_username,
        "email": "test@ex.com",
        "password": "password123",
    }
    with pytest.raises(ValidationError) as excinfo:
        UserSchema().load(data)
    assert "username" in excinfo.value.messages

    # empty username
    data["username"] = ""
    with pytest.raises(ValidationError):
        UserSchema().load(data)


def test_user_schema_password_min_length():
    # min 8 characters
    short_password = "a" * 7
    data = {"username": "user", "email": "test@ex.com", "password": short_password}
    with pytest.raises(ValidationError) as excinfo:
        UserSchema().load(data)
    assert "password" in excinfo.value.messages


def test_post_schema_load_success():
    data = {"content": "Test content"}
    result = PostSchema().load(data)
    assert result["content"] == "Test content"


def test_post_schema_content_boundary():
    # max 500 characters
    long_content = "a" * 501
    data = {"content": long_content}
    with pytest.raises(ValidationError) as excinfo:
        PostSchema().load(data)
    assert "content" in excinfo.value.messages

    # empty content
    data["content"] = ""
    with pytest.raises(ValidationError):
        PostSchema().load(data)


def test_setting_schema_load_success():
    data = {"theme": "dark", "notifications_enabled": False}
    result = SettingSchema().load(data)
    assert result["theme"] == "dark"
    assert result["notifications_enabled"] is False


def test_setting_schema_invalid_theme():
    data = {"theme": "invalid-theme"}
    with pytest.raises(ValidationError) as excinfo:
        SettingSchema().load(data)
    assert "theme" in excinfo.value.messages


def test_setting_schema_boolean_normalization():
    # Should handle strings like "true", "yes", "1"
    data = {"notifications_enabled": "true"}
    result = SettingSchema().load(data)
    assert result["notifications_enabled"] is True

    # Current implementation seems to check:
    # val.lower() in ("1", "true", "yes")
    data = {"notifications_enabled": "maybe"}
    result = SettingSchema().load(data)
    assert result["notifications_enabled"] is False


def test_user_schema_dump_hides_password():
    # Mock user object
    class MockUser:
        id = 1
        username = "test"
        email = "test@ex.com"
        password_hash = "secret"

    user = MockUser()
    result = UserSchema().dump(user)
    assert "username" in result
    assert "password" not in result
    assert "password_hash" not in result
