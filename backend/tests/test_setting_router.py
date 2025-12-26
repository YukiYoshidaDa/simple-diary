import json

import pytest

from services import user_service


@pytest.fixture
def auth_client(client, db):
    """ログイン済みのクライアントを提供"""
    user_data = {
        "username": "setrouter",
        "email": "setr@ex.com",
        "password": "password",
    }
    user = user_service.register_user(user_data)

    client.post(
        "/api/users/login",
        data=json.dumps({"username": "setrouter", "password": "password"}),
        content_type="application/json",
    )
    return client, user


def test_get_settings_api(auth_client):
    """API経由での設定取得を確認"""
    client, user = auth_client
    response = client.get("/api/settings")

    assert response.status_code == 200
    assert "theme" in response.get_json()


def test_update_settings_api(auth_client):
    """API経由での設定更新を確認"""
    client, user = auth_client
    response = client.patch(
        "/api/settings",
        data=json.dumps({"theme": "dark"}),
        content_type="application/json",
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Settings updated"
    assert data["settings"]["theme"] == "dark"
