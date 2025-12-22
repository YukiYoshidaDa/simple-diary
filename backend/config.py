import os

class Config:
    # 1. 動作環境の判定（Compose 側で指定した FLASK_ENV を参照）
    ENV = os.getenv("FLASK_ENV", "development")

    # 2. 秘密鍵の設定
    # 開発時はデフォルト値を、本番（FLASK_ENV=production）では「必須」にします
    if ENV == "development":
        SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    else:
        # 本番で SECRET_KEY がないとエラーを投げて起動させない（安全第一！）
        SECRET_KEY = os.environ.get("SECRET_KEY")
        if not SECRET_KEY:
            raise ValueError("No SECRET_KEY set for production environment")

    # 3. データベース接続文字列
    # Compose 側で注入した変数名を正確に使いましょう！
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql_sns")  # デフォルトはサービス名
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
    )

    # SQLAlchemy の追加設定（警告抑制など）
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 4. アプリケーションのデフォルト設定
    DEFAULT_THEME = os.getenv("DEFAULT_THEME", "light")
    DEFAULT_NOTIFICATIONS = os.getenv("DEFAULT_NOTIFICATIONS_ENABLED", "True") == "True"
