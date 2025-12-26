import pytest

from app import create_app
from config import Config
from extensions import db as _db


class TestConfig(Config):
    """テスト用の設定クラス"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    # Flask-Login の認証を有効にする（デフォルトで有効だが念のため）
    LOGIN_DISABLED = False


@pytest.fixture(scope="session")
def app():
    """テスト用のFlaskアプリケーションインスタンスを作成します。"""
    app = create_app(TestConfig)

    with app.app_context():
        yield app


@pytest.fixture(scope="function", autouse=True)
def db(app):
    """
    各テストでクリーンなデータベースセッションを提供します。
    autouse=True により、各テストの実行前に必ずテーブルが作成されます。
    """
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """APIのリクエストをシミュレーションするためのHTTPクライアントを提供します。"""
    return app.test_client()


@pytest.fixture
def registered_user(db):
    """テスト用に登録済みのユーザーを作成します。"""
    from services import user_service

    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
    }
    return user_service.register_user(user_data)


@pytest.fixture
def auth_client(client, registered_user):
    """ログイン済みのクライアントを提供します。"""
    import json

    client.post(
        "/api/users/login",
        data=json.dumps({"username": "testuser", "password": "password123"}),
        content_type="application/json",
    )
    return client
