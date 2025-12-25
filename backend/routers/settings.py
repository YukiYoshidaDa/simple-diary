from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from marshmallow import ValidationError

from schemas.setting_schema import SettingUpdateSchema
from services import setting_service

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("", methods=["GET"])
@login_required
def get_settings():
    settings = setting_service.get_settings_by_user(current_user.id)
    if not settings:
        return jsonify({"error": "Settings not found"}), 404

    return jsonify(settings.to_dict()), 200


@settings_bp.route("", methods=["PATCH"])
@login_required
def update_settings_route():
    try:
        body = request.get_json() or {}
        data = SettingUpdateSchema().load(body, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    updated_settings = setting_service.update_settings(current_user.id, data)

    if not updated_settings:
        return jsonify({"error": "Failed to update"}), 400

    return jsonify(
        {"message": "Settings updated", "settings": updated_settings.to_dict()}
    ), 200
