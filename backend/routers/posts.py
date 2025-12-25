from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from schemas.base import schema_with_context
from schemas.post_schema import PostSchema
from services import post_service

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/", methods=["POST"])
@login_required
def create_post():
    body = request.get_json() or {}
    post_obj = schema_with_context(PostSchema, current_user_id=current_user.id).load(
        body
    )

    post = post_service.create_post(post_obj)
    if not post:
        return jsonify({"error": "Failed to create post"}), 500
    return jsonify(PostSchema().dump(post)), 201


@posts_bp.route("/", methods=["GET"])
def get_all_posts():
    posts = post_service.get_all_posts()
    return jsonify(PostSchema(many=True).dump(posts)), 200


@posts_bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = post_service.get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(PostSchema().dump(post)), 200


@posts_bp.route("/<int:post_id>", methods=["PATCH"])
@login_required
def update_post(post_id):
    body = request.get_json() or {}

    post = post_service.get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if post.user_id != current_user.id:
        return jsonify({"error": "Forbidden"}), 403

    data_obj = schema_with_context(PostSchema, post=post).load(body, partial=True)

    updated = post_service.update_post(data_obj)
    if not updated:
        return jsonify({"error": "Failed to update post"}), 500

    return jsonify(PostSchema().dump(updated)), 200


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
