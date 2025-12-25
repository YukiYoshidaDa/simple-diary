from flask import current_app

from extensions import db
from models import Post


def create_post(post_obj):
    """Schema が作った Post インスタンスを受け取り保存する"""
    try:
        db.session.add(post_obj)
        db.session.commit()
        return post_obj
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


def update_post(post_obj):
    try:
        post = Post.query.get(post_obj.id)
        if post:
            post.content = post_obj.content
            db.session.commit()
            return post
        return None
    except Exception as e:
        current_app.logger.error(f"update_post error: {e}")
        db.session.rollback()
        return None
