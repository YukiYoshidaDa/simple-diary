def test_app_is_testing(app):
    """アプリケーションがテストモードで起動しているか確認"""
    assert app.config["TESTING"] is True


def test_db_connection(db):
    """データベース（SQLite memory）への接続を確認"""
    from sqlalchemy import text

    result = db.session.execute(text("SELECT 1"))
    assert result.fetchone()[0] == 1
