import pytest

from exceptions import ForbiddenError, NotFoundError
from models import Setting
from services import setting_service, user_service


@pytest.fixture
def test_user(db):
    """テスト用のユーザーを作成（初期設定も作成されるはず）"""
    data = {"username": "setuser", "email": "set@example.com", "password": "password"}
    return user_service.register_user(data)


def test_create_default_settings(db):
    """初期設定が正しく作成されるか確認"""
    user = user_service.register_user(
        {"username": "inituser", "email": "init@ex.com", "password": "p"}
    )
    # register_user 内で create_default_settings が呼ばれる想定
    settings = Setting.query.filter_by(user_id=user.id).first()
    assert settings is not None
    assert settings.theme == "light"  # Configのデフォルト想定


def test_get_settings_by_user_success(db, test_user):
    """ユーザー設定が取得できることを確認"""
    settings = setting_service.get_settings_by_user(test_user.id)
    assert settings.user_id == test_user.id


def test_get_settings_by_user_not_found(db):
    """存在しないユーザーの設定取得でNotFoundErrorが発生することを確認"""
    with pytest.raises(NotFoundError):
        setting_service.get_settings_by_user(999)


def test_update_settings_success(db, test_user):
    """設定の更新が成功することを確認"""
    updated = setting_service.update_settings(
        test_user.id, {"theme": "dark", "notifications_enabled": False}, test_user.id
    )
    assert updated.theme == "dark"
    assert updated.notifications_enabled is False


def test_update_settings_forbidden(db, test_user):
    """他人の設定を更新しようとするとForbiddenErrorが発生することを確認"""
    other_user = user_service.register_user(
        {"username": "other_set", "email": "other_set@ex.com", "password": "p"}
    )
    with pytest.raises(ForbiddenError):
        setting_service.update_settings(test_user.id, {"theme": "dark"}, other_user.id)
