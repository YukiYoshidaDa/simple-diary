from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from services import post_service

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/", methods=["POST"])
@login_required
def create_post():
    data = request.get_json() or {}
    content = (data.get("content") or "").strip()

    if not content:
        return jsonify({"error": "Content is required"}), 400
    if len(content) > 2000:
        return jsonify({"error": "Content too long"}), 400

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
    data = request.get_json() or {}
    new_content = (data.get("content") or "").strip()

    if not new_content:
        return jsonify({"error": "Content is required"}), 400
    if len(new_content) > 2000:
        return jsonify({"error": "Content too long"}), 400

    post = post_service.get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if post.user_id != current_user.id:
        return jsonify({"error": "Forbidden"}), 403

    updated = post_service.update_post(post_id, new_content)
    if not updated:
        return jsonify({"error": "Failed to update post"}), 500

    return jsonify(updated.to_dict()), 200


@posts_bp.route("/<int:post_id>", methods=["DELETE"])
@login_required
def delete_post(post_id):
    post = post_service.get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if post.user_id != current_user.id:
        return jsonify({"error": "Forbidden"}), 403

    success = post_service.delete_post(post_id)
    if not success:
        return jsonify({"error": "Failed to delete post"}), 500
    return jsonify({"message": "Post deleted successfully"}), 200
