import json


def test_register_api_success(client):
    """API経由でのユーザー登録成功を確認"""
    response = client.post(
        "/api/users/register",
        data=json.dumps(
            {
                "username": "apiuser",
                "email": "api@example.com",
                "password": "apipassword",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully"
    assert "id" in data


def test_login_api_success(client, db):
    """API経由でのログイン成功を確認"""
    # 先にユーザーを登録
    from services import user_service

    user_service.register_user(
        {
            "username": "loginapi",
            "email": "loginapi@example.com",
            "password": "loginpass",
        }
    )

    response = client.post(
        "/api/users/login",
        data=json.dumps({"username": "loginapi", "password": "loginpass"}),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Login successful"


def test_get_profile_unauthorized(client):
    """未ログイン状態でプロフィール取得を試みた場合に401エラーになることを確認"""
    response = client.get("/api/users/profile")
    assert response.status_code == 401


def test_full_login_profile_flow(client, db):
    """ログインからプロフィール取得までのフローを確認"""
    # 1. 登録
    client.post(
        "/api/users/register",
        data=json.dumps(
            {
                "username": "flowuser",
                "email": "flow@example.com",
                "password": "flowpass",
            }
        ),
        content_type="application/json",
    )

    # 2. ログイン
    client.post(
        "/api/users/login",
        data=json.dumps({"username": "flowuser", "password": "flowpass"}),
        content_type="application/json",
    )

    # 3. プロフィール取得 (セッションが維持されているか)
    response = client.get("/api/users/profile")
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "flowuser"
    assert data["email"] == "flow@example.com"


def test_update_profile_api(auth_client):
    """API経由でのプロフィール更新を確認"""
    response = auth_client.patch(
        "/api/users/profile",
        data=json.dumps({"username": "newname"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.get_json()["user"]["username"] == "newname"


def test_delete_account_api(auth_client):
    """API経由でのアカウント削除を確認"""
    response = auth_client.delete("/api/users/profile")
    assert response.status_code == 200

    # 削除後はログインできないことを確認
    login_response = auth_client.post(
        "/api/users/login",
        data=json.dumps({"username": "testuser", "password": "password123"}),
        content_type="application/json",
    )
    assert login_response.status_code == 401
