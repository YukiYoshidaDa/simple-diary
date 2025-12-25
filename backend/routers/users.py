from flask import Blueprint, jsonify, request
from flask_login import (
    current_user,
    login_required,
    logout_user,
)
from flask_login import (
    login_user as flask_login_user,
)

from schemas.post_schema import PostSchema
from schemas.user_schema import LoginSchema, UpdateUserSchema, UserSchema
from services import post_service, user_service

users_bp = Blueprint("users", __name__)


# ユーザー登録
@users_bp.route("/register", methods=["POST"])
def register():
    body = request.get_json() or {}
    data = UserSchema().load(body)

    username = data["username"]
    email = data["email"]
    password = data["password"]

    # 重複チェック
    if user_service.user_exists_by_username(username):
        return jsonify({"message": "Username already taken"}), 409
    if user_service.user_exists_by_email(email):
        return jsonify({"message": "Email already registered"}), 409

    user = user_service.register_user(username, email, password)
    if not user:
        return jsonify({"message": "Failed to register user"}), 500

    return jsonify({"message": "User registered successfully", "id": user.id}), 201


@users_bp.route("/login", methods=["POST"])
def login():
    body = request.get_json() or {}
    data = LoginSchema().load(body)

    user = user_service.login_user(data["username"], data["password"])
    if user:
        flask_login_user(user)
        return jsonify({"message": "Login successful", "id": user.id}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@users_bp.route("/all", methods=["GET"])
def all_users():
    users = user_service.get_all_users()
    return jsonify(UserSchema(many=True).dump(users)), 200


@users_bp.route("/profile", methods=["GET"])
@login_required
def get_profile():
    return jsonify(
        {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
        }
    )


@users_bp.route("/profile", methods=["PATCH"])
@login_required
def patch_profile():
    """ユーザー情報の部分更新"""
    body = request.get_json() or {}
    data = UpdateUserSchema().load(body, partial=True)

    # 重複チェック
    if (
        "email" in data
        and data.get("email")
        and data.get("email") != current_user.email
    ):
        if user_service.user_exists_by_email(data.get("email")):
            return jsonify({"message": "Email already in use"}), 409

    if (
        "username" in data
        and data.get("username")
        and data.get("username") != current_user.username
    ):
        if user_service.user_exists_by_username(data.get("username")):
            return jsonify({"message": "Username already in use"}), 409

    updated_user = user_service.update_user_profile(current_user.id, data)

    if updated_user:
        return jsonify(
            {"message": "Profile updated", "user": UserSchema().dump(updated_user)}
        ), 200
    else:
        return jsonify({"message": "Failed to update profile"}), 400


@users_bp.route("/profile", methods=["DELETE"])
@login_required
def delete_profile():
    user_service.delete_user(current_user.id)
    return jsonify({"message": "Profile deleted successfully"}), 200


@users_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


@users_bp.route("/<int:user_id>/posts", methods=["GET"])
def get_user_posts_route(user_id):
    posts = post_service.get_posts_by_user(user_id)
    return jsonify(PostSchema(many=True).dump(posts)), 200
