from models import Post, db


def create_post(user_id, content):
    """新しい投稿を作成"""
    post = Post(user_id=user_id, content=content)
    db.session.add(post)
    db.session.commit()
    return post


def get_post_by_id(post_id):
    return Post.query.get(post_id)


def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return True
    return False


def get_all_posts():
    return Post.query.all()


def get_posts_by_user(user_id):
    return Post.query.filter_by(user_id=user_id).all()


def update_post(post_id, new_content):
    post = Post.query.get(post_id)
    if post:
        post.content = new_content
        db.session.commit()
        return post
    return None
