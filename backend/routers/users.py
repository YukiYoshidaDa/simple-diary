from flask import Blueprint, jsonify, request
from flask_login import (
    current_user,
    login_required,
    logout_user,
)
from flask_login import (
    login_user as flask_login_user,
)

from services import post_service, user_service

users_bp = Blueprint("users", __name__)


# ユーザー登録
@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    user = user_service.register_user(username, email, password)
    if not user:
        return jsonify({"message": "User already exists"}), 400

    return jsonify({"message": "User registered successfully", "id": user.id}), 201


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = user_service.login_user(username, password)
    if user:
        flask_login_user(user)
        return jsonify({"message": "Login successful", "id": user.id}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@users_bp.route("/all", methods=["GET"])
def all_users():
    users = user_service.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200


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
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    updated_user = user_service.update_user_profile(current_user.id, data)

    if updated_user:
        return jsonify(
            {"message": "Profile updated", "user": updated_user.to_dict()}
        ), 200
    else:
        return jsonify({"message": "User not found"}), 404


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
    return jsonify([post.to_dict() for post in posts]), 200
