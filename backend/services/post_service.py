from flask import current_app

from exceptions import ForbiddenError, NotFoundError
from extensions import db
from models import Post


def create_post(validated_data: dict, current_user_id: int):
    try:
        post = Post(content=validated_data.get("content"), user_id=current_user_id)
        db.session.add(post)
        db.session.commit()
        return post
    except Exception as e:
        current_app.logger.error(f"create_post error: {e}")
        db.session.rollback()
        raise  # 予期せぬエラーもraiseして500系として扱う


def get_post_by_id(post_id):
    post = Post.query.get(post_id)
    if not post:
        raise NotFoundError(f"Post with id {post_id} not found")
    return post


def delete_post(post_id: int, current_user_id: int):
    # 存在チェックと権限チェックをサービス側で統合！
    post = get_post_by_id(post_id)
    if post.user_id != current_user_id:
        raise ForbiddenError("You do not have permission to delete this post")

    try:
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"delete_post error: {e}")
        db.session.rollback()
        raise


def get_all_posts():
    return Post.query.all()


def update_post(post_id: int, validated_data: dict, current_user_id: int):
    # 共通のget_post_by_idを使うことで存在チェックを自動化
    post = get_post_by_id(post_id)

    if post.user_id != current_user_id:
        raise ForbiddenError("You do not have permission to update this post")

    try:
        if "content" in validated_data:
            post.content = validated_data["content"]
        db.session.commit()
        return post
    except Exception as e:
        current_app.logger.error(f"update_post error: {e}")
        db.session.rollback()
        raise
