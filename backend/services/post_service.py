from flask import current_app

from exceptions import ForbiddenError, NotFoundError
from extensions import db
from models import Post


def create_post(validated_data: dict, current_user_id: int):
    """Create a Post from validated data and associate current user as owner."""
    try:
        post = Post(content=validated_data.get("content"), user_id=current_user_id)
        db.session.add(post)
        db.session.commit()
        return post
    except Exception as e:
        current_app.logger.error(f"create_post error: {e}")
        db.session.rollback()
        return None


def get_post_by_id(post_id):
    return Post.query.get(post_id)


def delete_post(post_id):
    try:
        post = Post.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return True
        return False
    except Exception as e:
        current_app.logger.error(f"delete_post error: {e}")
        db.session.rollback()
        return False


def get_all_posts():
    return Post.query.all()


def get_posts_by_user(user_id):
    return Post.query.filter_by(user_id=user_id).all()


def update_post(post_id: int, validated_data: dict, current_user_id: int):
    try:
        post = Post.query.get(post_id)
        if not post:
            raise NotFoundError("Post not found")

        if post.user_id != current_user_id:
            raise ForbiddenError("Forbidden")

        if "content" in validated_data:
            post.content = validated_data["content"]

        db.session.commit()
        return post
    except (NotFoundError, ForbiddenError):
        raise
    except Exception as e:
        current_app.logger.error(f"update_post error: {e}")
        db.session.rollback()
        return None
