import os

from flask import Blueprint, Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import text

from models import User, db
from routers import posts_bp, settings_bp, users_bp

# Flaskアプリケーションのインスタンス作成
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"

CORS(app)  # Reactからのリクエストを許可するためにCORSを設定


SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}"
    f"@{os.environ['MYSQL_HOST']}:{os.environ['MYSQL_PORT']}/{os.environ['MYSQL_DATABASE']}"
)

# MySQL接続設定 (root password, データベース名の設定)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# SQLAlchemyインスタンス作成
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"message": "Unauthorized"}), 401


@app.route("/")
def hello_world():
    try:
        # DB接続テスト
        result = db.session.execute(text("SELECT 1"))
        return "DB connection successful: " + str(result.fetchone())
    except Exception as e:
        return "Error: " + str(e)


api_bp = Blueprint("api", __name__)

api_bp.register_blueprint(users_bp, url_prefix="/users")
api_bp.register_blueprint(settings_bp, url_prefix="/settings")
api_bp.register_blueprint(posts_bp, url_prefix="/posts")
app.register_blueprint(api_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
