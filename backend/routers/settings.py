from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import Setting, db

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    # ユーザーの設定を取得
    settings = Setting.query.filter_by(user_id=current_user.id).first()

    if request.method == "POST":
        # フォームデータを取得して設定を更新
        notifications_enabled = request.form.get("notifications_enabled") == "on"
        language = request.form.get("language")

        if settings:
            settings.notifications_enabled = notifications_enabled
            settings.language = language
        else:
            # 設定がまだ存在しない場合、新たに作成
            new_settings = Setting(
                user_id=current_user.id,
                notifications_enabled=notifications_enabled,
                language=language,
            )
            db.session.add(new_settings)

        db.session.commit()

        return redirect(url_for("settings.settings"))

    return render_template("settings.html", settings=settings)
