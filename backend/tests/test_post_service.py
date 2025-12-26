import pytest

from exceptions import ForbiddenError, NotFoundError
from models import Post
from services import post_service, user_service


@pytest.fixture
def test_user(db):
    """テスト用のユーザーを作成"""
    data = {"username": "postuser", "email": "post@example.com", "password": "password"}
    return user_service.register_user(data)


def test_create_post_success(db, test_user):
    """日記の投稿が成功することを確認"""
    data = {"content": "Hello, world!"}
    post = post_service.create_post(data, test_user.id)

    assert post.id is not None
    assert post.content == "Hello, world!"
    assert post.user_id == test_user.id
    assert db.session.get(Post, post.id) is not None


def test_get_post_by_id_success(db, test_user):
    """IDで日記が取得できることを確認"""
    post = post_service.create_post({"content": "Find me"}, test_user.id)
    retrieved = post_service.get_post_by_id(post.id)
    assert retrieved.content == "Find me"


def test_get_post_by_id_not_found(db):
    """存在しないIDでNotFoundErrorが発生することを確認"""
    with pytest.raises(NotFoundError):
        post_service.get_post_by_id(999)


def test_update_post_success(db, test_user):
    """日記の更新が成功することを確認"""
    post = post_service.create_post({"content": "Old content"}, test_user.id)
    updated = post_service.update_post(
        post.id, {"content": "New content"}, test_user.id
    )

    assert updated.content == "New content"
    assert db.session.get(Post, post.id) is not None
    assert db.session.get(Post, post.id).content == "New content"


def test_update_post_forbidden(db, test_user):
    """他人の日記を更新しようとするとForbiddenErrorが発生することを確認"""
    other_user = user_service.register_user(
        {"username": "other", "email": "other@example.com", "password": "pass"}
    )
    post = post_service.create_post({"content": "My post"}, test_user.id)

    with pytest.raises(ForbiddenError):
        post_service.update_post(post.id, {"content": "Hacked"}, other_user.id)


def test_delete_post_success(db, test_user):
    """日記の削除が成功することを確認"""
    post = post_service.create_post({"content": "Delete me"}, test_user.id)
    post_service.delete_post(post.id, test_user.id)

    assert db.session.get(Post, post.id) is None


def test_delete_post_forbidden(db, test_user):
    """他人の日記を削除しようとするとForbiddenErrorが発生することを確認"""
    other_user = user_service.register_user(
        {"username": "other_del", "email": "other_del@example.com", "password": "pass"}
    )
    post = post_service.create_post({"content": "My post"}, test_user.id)

    with pytest.raises(ForbiddenError):
        post_service.delete_post(post.id, other_user.id)


def test_get_all_posts(db, test_user):
    """全日記を取得できることを確認"""
    post_service.create_post({"content": "Post 1"}, test_user.id)
    post_service.create_post({"content": "Post 2"}, test_user.id)

    posts = post_service.get_all_posts()
    assert len(posts) >= 2
