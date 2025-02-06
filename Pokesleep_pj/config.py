import os

class Config:
    # Flask�̃Z�b�V�����L�[
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))  # ���ϐ�����閧�����擾

    # �f�[�^�x�[�X�ڑ��ݒ�
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://localhost/pokesleep_db'  # ���[�J���J���p�f�[�^�x�[�XURL
    )

    # SQLAlchemy�̐ݒ�
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # �Z�b�V�����ݒ�
    SESSION_COOKIE_NAME = 'pokesleep_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv('RENDER', False) == 'True'  # Render���Ȃ�True

    # Flask�̃f�o�b�O�ݒ�
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

    # ���M���O�ݒ�
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
