from models import User, db


def register_user(username, email, password):
    """ユーザーを登録"""
    if (
        User.query.filter_by(username=username).first()
        or User.query.filter_by(email=email).first()
    ):
        return None  # ユーザーが既に存在する場合は None を返す

    new_user = User(username=username, email=email)
    new_user.set_password(password)  # パスワードをハッシュ化して保存
    db.session.add(new_user)
    db.session.commit()
    return new_user


def login_user(username, password):
    """ログイン処理"""
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None


def get_all_users():
    """全ユーザーを取得"""
    return User.query.all()


def get_user_by_id(user_id):
    """IDでユーザーを取得"""
    return User.query.get(user_id)


def update_user_profile(user_id, new_username=None, new_email=None):
    """ユーザー情報を更新"""
    user = User.query.get(user_id)
    if not user:
        return None

    if new_username is not None:
        user.username = new_username
    if new_email is not None:
        user.email = new_email

    db.session.commit()
    return user


def delete_user(user_id):
    """ユーザーを削除"""
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
