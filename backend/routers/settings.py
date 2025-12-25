from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from schemas.base import schema_with_context
from schemas.setting_schema import SettingSchema
from services import setting_service

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("", methods=["GET"])
@login_required
def get_settings():
    settings = setting_service.get_settings_by_user(current_user.id)
    if not settings:
        return jsonify({"error": "Settings not found"}), 404

    return jsonify(SettingSchema().dump(settings)), 200


@settings_bp.route("", methods=["PATCH"])
@login_required
def update_settings_route():
    body = request.get_json() or {}
    settings_obj = schema_with_context(
        SettingSchema,
        current_user_id=current_user.id,
        settings=setting_service.get_settings_by_user(current_user.id),
    ).load(body, partial=True)

    updated_settings = setting_service.update_settings(settings_obj)

    if not updated_settings:
        return jsonify({"error": "Failed to update"}), 400

    return jsonify(
        {
            "message": "Settings updated",
            "settings": SettingSchema().dump(updated_settings),
        }
    ), 200
