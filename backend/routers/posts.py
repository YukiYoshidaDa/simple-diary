from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from services import post_service

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/", methods=["POST"])
@login_required
def create_post():
    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "Content is required"}), 400

    post = post_service.create_post(user_id=current_user.id, content=content)
    return jsonify(post.to_dict()), 201


@posts_bp.route("/", methods=["GET"])
def get_all_posts():
    posts = post_service.get_all_posts()
    return jsonify([post.to_dict() for post in posts]), 200


@posts_bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = post_service.get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post.to_dict()), 200


@posts_bp.route("/<int:post_id>", methods=["PATCH"])
@login_required
def update_post(post_id):
    data = request.get_json()
    new_content = data.get("content")

    if not new_content:
        return jsonify({"error": "Content is required"}), 400

    post = post_service.update_post(post_id, new_content)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    return jsonify(post.to_dict()), 200


@posts_bp.route("/<int:post_id>", methods=["DELETE"])
@login_required
def delete_post(post_id):
    success = post_service.delete_post(post_id)
    if not success:
        return jsonify({"error": "Post not found"}), 404
    return jsonify({"message": "Post deleted successfully"}), 200
