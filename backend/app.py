from flask import Blueprint, Flask, jsonify
from flask_cors import CORS
from sqlalchemy import text

from config import Config
from extensions import db, login_manager, migrate


def create_app(config_object: object = Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    CORS(app)

    # 拡張の初期化
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # ルーターの登録は遅延インポートで循環参照を回避
    from routers import posts_bp, settings_bp, users_bp

    api_bp = Blueprint("api", __name__)
    api_bp.register_blueprint(users_bp, url_prefix="/users")
    api_bp.register_blueprint(settings_bp, url_prefix="/settings")
    api_bp.register_blueprint(posts_bp, url_prefix="/posts")
    app.register_blueprint(api_bp, url_prefix="/api")

    # ドメインエラーのハンドラ登録
    register_error_handlers(app)

    @login_manager.user_loader
    def load_user(user_id):
        # ロード時にモデルをインポートして循環を避ける
        from models import User

        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"message": "Unauthorized"}), 401

    @app.route("/")
    def hello_world():
        try:
            result = db.session.execute(text("SELECT 1"))
            return "DB connection successful: " + str(result.fetchone())
        except Exception as e:
            return "Error: " + str(e)

    from marshmallow import ValidationError

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return jsonify({"errors": err.messages}), 400

    return app


def register_error_handlers(app: Flask):
    """Register domain error handlers on the Flask app."""
    # import exceptions locally to avoid circular imports at module import time
    from exceptions import DomainError, ForbiddenError, NotFoundError, UnauthorizedError

    @app.errorhandler(NotFoundError)
    def handle_not_found(err):
        return jsonify({"error": str(err)}), 404

    @app.errorhandler(ForbiddenError)
    def handle_forbidden(err):
        return jsonify({"error": str(err)}), 403

    @app.errorhandler(DomainError)
    def handle_domain_error(err):
        # Generic handler for other domain errors; default to 400
        return jsonify({"error": str(err)}), 400

    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized_error(e):
        return jsonify({"error": "Unauthorized", "message": str(e)}), 401


app = create_app()
