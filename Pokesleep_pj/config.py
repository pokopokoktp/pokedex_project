import os

class Config:
    # Flaskのセッションキー
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))  # 環境変数から秘密鍵を取得

    # データベース接続設定
    # RenderでのデータベースURLを環境変数から取得し、デフォルトのローカル接続URLを設定
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://pokesleep_db_user:g6qrdTzAzjwViN7ywKbHEN1gjbpxZOmC@dpg-cuibpp2j1k6c73as74tg-a.singapore-postgres.render.com/pokesleep_db'
    )

    # SQLAlchemyの設定
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 無駄な変更追跡をオフに

    # セッション設定
    SESSION_COOKIE_NAME = 'pokesleep_session'
    SESSION_COOKIE_HTTPONLY = True  # クライアント側からのアクセスを制限
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True'  # HTTPS接続時のみクッキーが送信されるように

    # Flaskのデバッグ設定（環境に合わせて切り替える）
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

    # ロギング設定（必要に応じて追加）
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')  # ログレベル設定

    # その他必要な設定
    # 例: APIキーや外部サービスのURLなど
    # SOME_API_KEY = os.getenv('SOME_API_KEY')
    # EXTERNAL_SERVICE_URL = os.getenv('EXTERNAL_SERVICE_URL')
