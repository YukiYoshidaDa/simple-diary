import json

from services import post_service, user_service

# Local auth_client removed, using conftest.py's auth_client instead


def test_create_post_api(auth_client):
    """API経由での日記投稿を確認"""
    response = auth_client.post(
        "/api/posts/",
        data=json.dumps({"content": "API post content"}),
        content_type="application/json",
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["content"] == "API post content"


def test_get_all_posts_api(client, db):
    """API経由での全日記取得を確認"""
    user = user_service.register_user(
        {"username": "p1", "email": "p1@ex.com", "password": "p"}
    )
    post_service.create_post({"content": "Post A"}, user.id)

    response = client.get("/api/posts/")
    assert response.status_code == 200
    assert len(response.get_json()) >= 1


def test_get_single_post_api(client, db):
    """API経由での個別日記取得を確認"""
    user = user_service.register_user(
        {"username": "p2", "email": "p2@ex.com", "password": "p"}
    )
    post = post_service.create_post({"content": "Single post"}, user.id)

    response = client.get(f"/api/posts/{post.id}")
    assert response.status_code == 200
    assert response.get_json()["content"] == "Single post"


def test_update_post_api(auth_client, registered_user):
    """API経由での日記更新を確認"""
    post = post_service.create_post({"content": "Old"}, registered_user.id)

    response = auth_client.patch(
        f"/api/posts/{post.id}",
        data=json.dumps({"content": "New"}),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.get_json()["content"] == "New"


def test_delete_post_api(auth_client, registered_user):
    """API経由での日記削除を確認"""
    post = post_service.create_post({"content": "Goodbye"}, registered_user.id)

    response = auth_client.delete(f"/api/posts/{post.id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Post deleted successfully"


def test_post_authorization_api(client, db):
    """他人の投稿を操作できないことを確認（APIレベル）"""
    # 第一のユーザー
    user1 = user_service.register_user(
        {"username": "u1", "email": "u1@ex.com", "password": "p"}
    )
    post = post_service.create_post({"content": "User1's post"}, user1.id)

    # 第二のユーザーでログイン
    user_service.register_user(
        {"username": "u2", "email": "u2@ex.com", "password": "p"}
    )
    client.post(
        "/api/users/login",
        data=json.dumps({"username": "u2", "password": "p"}),
        content_type="application/json",
    )

    # 他人の投稿を更新しようとする
    response = client.patch(
        f"/api/posts/{post.id}",
        data=json.dumps({"content": "Hacked"}),
        content_type="application/json",
    )
    assert response.status_code == 403

    # 他人の投稿を削除しようとする
    response = client.delete(f"/api/posts/{post.id}")
    assert response.status_code == 403
