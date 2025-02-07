from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# dbインスタンスを作成
db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    pokemons = db.relationship("UserPokemon", back_populates="user")
    diaries = db.relationship("SleepDiary", back_populates="user")

    # パスワードの検証を行うメソッドを追加
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sleep_type = db.Column(db.String(50), nullable=False)
    specialty = db.Column(db.String(50), nullable=False)
    main_skill = db.Column(db.String(100), nullable=False)

    owners = db.relationship("UserPokemon", back_populates="pokemon")

class UserPokemon(db.Model):
    __tablename__ = 'user_pokemon'

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id', ondelete='CASCADE'))
    caught_date = db.Column(db.Date)

    user = db.relationship("User", back_populates="pokemons")
    pokemon = db.relationship("Pokemon", back_populates="owners")

class SleepDiary(db.Model):
    __tablename__ = 'sleep_diary'

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    date = db.Column(db.Date, nullable=False)
    sleep_quality = db.Column(db.String(50))
    memo = db.Column(db.String)

    user = db.relationship("User", back_populates="diaries")
