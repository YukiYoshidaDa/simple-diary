from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from schemas.setting_schema import SettingSchema
from services import setting_service

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("", methods=["GET"])
@login_required
def get_settings():
    settings = setting_service.get_settings_by_user(current_user.id)
    return jsonify(SettingSchema().dump(settings)), 200


@settings_bp.route("", methods=["PATCH"])
@login_required
def update_settings_route():
    body = request.get_json() or {}
    validated = SettingSchema(partial=True).load(body)

    updated_settings = setting_service.update_settings(
        current_user.id, validated, current_user.id
    )

    return (
        jsonify(
            {
                "message": "Settings updated",
                "settings": SettingSchema().dump(updated_settings),
            }
        ),
        200,
    )
