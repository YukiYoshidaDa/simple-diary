from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from schemas.post_schema import PostSchema
from services import post_service

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/", methods=["POST"])
@login_required
def create_post():
    body = request.get_json() or {}
    validated = PostSchema().load(body)
    post = post_service.create_post(validated, current_user.id)
    return jsonify(PostSchema().dump(post)), 201


@posts_bp.route("/", methods=["GET"])
def get_all_posts():
    posts = post_service.get_all_posts()
    return jsonify(PostSchema(many=True).dump(posts)), 200


@posts_bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    # 存在しなければ自動で NotFoundError -> 404
    post = post_service.get_post_by_id(post_id)
    return jsonify(PostSchema().dump(post)), 200


@posts_bp.route("/<int:post_id>", methods=["PATCH"])
@login_required
def update_post(post_id):
    body = request.get_json() or {}
    validated = PostSchema(partial=True).load(body)
    # 権限エラーもNotFoundもServiceが投げてくれる
    updated = post_service.update_post(post_id, validated, current_user.id)
    return jsonify(PostSchema().dump(updated)), 200


@posts_bp.route("/<int:post_id>", methods=["DELETE"])
@login_required
def delete_post(post_id):
    # パラメータに current_user.id を渡すのがポイント
    post_service.delete_post(post_id, current_user.id)
    return jsonify({"message": "Post deleted successfully"}), 200
