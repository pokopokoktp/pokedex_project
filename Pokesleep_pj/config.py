import os

class Config:
    # Flaskのセッションキー
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))  # 環境変数から秘密鍵を取得

    # データベース接続設定
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://localhost/pokesleep_db'  # ローカル開発用データベースURL
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
