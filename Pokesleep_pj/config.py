import os

class Config:
    # Flask�̃Z�b�V�����L�[
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))  # ���ϐ�����閧�����擾

    # �f�[�^�x�[�X�ڑ��ݒ�
    # Render�ł̃f�[�^�x�[�XURL�����ϐ�����擾���A�f�t�H���g�̃��[�J���ڑ�URL��ݒ�
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://pokesleep_db_user:g6qrdTzAzjwViN7ywKbHEN1gjbpxZOmC@dpg-cuibpp2j1k6c73as74tg-a.singapore-postgres.render.com/pokesleep_db'
    )

    # SQLAlchemy�̐ݒ�
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # ���ʂȕύX�ǐՂ��I�t��

    # �Z�b�V�����ݒ�
    SESSION_COOKIE_NAME = 'pokesleep_session'
    SESSION_COOKIE_HTTPONLY = True  # �N���C�A���g������̃A�N�Z�X�𐧌�
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True'  # HTTPS�ڑ����̂݃N�b�L�[�����M�����悤��

    # Flask�̃f�o�b�O�ݒ�i���ɍ��킹�Đ؂�ւ���j
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

    # ���M���O�ݒ�i�K�v�ɉ����Ēǉ��j
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')  # ���O���x���ݒ�

    # ���̑��K�v�Ȑݒ�
    # ��: API�L�[��O���T�[�r�X��URL�Ȃ�
    # SOME_API_KEY = os.getenv('SOME_API_KEY')
    # EXTERNAL_SERVICE_URL = os.getenv('EXTERNAL_SERVICE_URL')
