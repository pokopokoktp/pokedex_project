import os

class Config:
    # Flaskのセッションキー
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))  # 環境変数から秘密鍵を取得

    # データベース接続設定
    # RenderでのデータベースURLを環境変数から取得、デフォルトにSSLモードを追加
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://pokesleep_db_user:g6qrdTzAzjwViN7ywKbHEN1gjbpxZOmC@dpg-cuibpp2j1k6c73as74tg-a.singapore-postgres.render.com/pokesleep_db?sslmode=require'
    )

    # SQLAlchemyの設定
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # セッション設定
    SESSION_COOKIE_NAME = 'pokesleep_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv('RENDER', False) == 'True'  # Render環境ならTrue

    # Flaskのデバッグ設定
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

    # ロギング設定
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
