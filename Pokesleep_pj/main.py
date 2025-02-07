# -*- coding: utf-8 -*-  
from flask import Flask, request, render_template, redirect, url_for, session, flash 
from flask_login import LoginManager, login_user, login_required, logout_user, current_user 
from flask_migrate import Migrate 
from werkzeug.security import generate_password_hash, check_password_hash 
from .models import User, Pokemon, UserPokemon, SleepDiary, db
from .crud import create_user, create_pokemon, get_pokemon_list, catch_pokemon, create_sleep_diary, get_user_pokemons
from .database import SessionLocal, engine
from . import config  # config.pyをインポート
import os  # osモジュールをインポート

app = Flask(__name__)

DATABASE_URI = os.getenv("DATABASE_URL")

# SECRET_KEYの設定
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))  # 環境変数から取得、ない場合はランダム生成

# config.pyから設定を読み込む
app.config.from_object(config)

# DBマイグレーション
migrate = Migrate(app, db)

# Flask-Login の初期化
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ユーザーをロードする関数
@login_manager.user_loader
def load_user(user_id):
    try:
        with SessionLocal() as session_db:
            user = session_db.get(User, int(user_id))  # session.get() を使用
        return user
    except Exception as e:
        app.logger.error(f"ユーザーのロード中にエラー: {str(e)}")
        flash(f"エラーが発生しました: {str(e)}", 'error')
        return None

# ログイン機能
@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('index.html')  # タイトル画面

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with SessionLocal() as session_db:
            user = session_db.query(User).filter(User.username == username).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('ログインに成功しました！')
                return redirect(url_for('home'))  # ログイン後にホーム画面にリダイレクト
            else:
                flash('ユーザー名またはパスワードが正しくありません')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました', 'success')
    return redirect(url_for('index'))  # ログアウト後はタイトル画面へリダイレクト

# ホーム画面
@app.route('/home')
@login_required
def home():
    return render_template('home.html', is_admin=current_user.is_admin)

# ポケモン一覧
@app.route('/pokemon_list')
@login_required
def pokemon_list():
    try:
        with SessionLocal() as session_db:
            pokemons = get_pokemon_list(session_db)
            user_pokemons = get_user_pokemons(session_db, current_user.id)
            caught_pokemon_ids = [up.id for up in user_pokemons]  # Pokemonのidを参照

            user_pokemon_names = [pokemon.name for pokemon in user_pokemons]
            app.logger.info(f"全ポケモン: {[pokemon.name for pokemon in pokemons]}")
            app.logger.info(f"ユーザーが獲得したポケモン: {user_pokemon_names}.")

        return render_template('pokemon_list.html', pokemons=pokemons, caught_pokemon_ids=caught_pokemon_ids)
    except Exception as e:
        app.logger.error(f"ポケモンリスト取得中にエラー: {str(e)}")
        flash(f"エラーが発生しました: {str(e)}", 'error')
        return redirect(url_for('home'))

# ポケモンを捕獲
@app.route('/catch_pokemon/<int:pokemon_id>', methods=['POST'])
@login_required
def catch_pokemon_route(pokemon_id):
    try:
        with SessionLocal() as session_db:
            catch_pokemon(session_db, current_user.id, pokemon_id)
        flash('ポケモンを獲得しました！', 'success')
        return redirect(url_for('pokemon_list'))
    except Exception as e:
        app.logger.error(f"ポケモン獲得中にエラー: {str(e)}")
        flash(f"ポケモンを獲得できませんでした: {str(e)}", 'error')
        return redirect(url_for('pokemon_list'))

# 管理者専用のデコレーター
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            flash("管理者権限が必要です。", 'error')
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/add_pokemon', methods=['GET', 'POST'])
@admin_required
def add_pokemon():
    if request.method == 'POST':
        name = request.form['name']
        number = int(request.form['number'])
        sleep_type = request.form['sleep_type']
        specialty = request.form['specialty']
        main_skill = request.form['main_skill']

        if not name or not sleep_type or not specialty or not main_skill or not number:
            flash('すべてのフィールドを入力してください。', 'error')
            return render_template('add_pokemon.html')

        with SessionLocal() as session_db:
            try:
                create_pokemon(session_db, name, number, sleep_type, specialty, main_skill)
                session_db.commit()
                flash('ポケモンを追加しました！')
            except Exception as e:
                app.logger.error(f"ポケモン追加中にエラー: {str(e)}")
                flash(f"エラーが発生しました: {str(e)}", 'error')

        return redirect(url_for('pokemon_list'))

    return render_template('add_pokemon.html')

# ユーザー登録機能
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='scrypt', salt_length=16)

        with SessionLocal() as session_db:
            if session_db.query(User).filter(User.username == username).first():
                flash('すでに存在するユーザー名です。')
            else:
                create_user(session_db, username, hashed_password)
                flash('ユーザー登録が完了しました！')
                return redirect(url_for('login'))

    return render_template('register.html')

# 睡眠日記のリスト表示
@app.route('/sleep_diary_list', methods=['GET'])
@login_required
def sleep_diary_list():
    try:
        with SessionLocal() as session_db:
            diaries = session_db.query(SleepDiary).filter(SleepDiary.user_id == current_user.id).all()
        return render_template('sleep_diary_list.html', diaries=diaries)
    except Exception as e:
        app.logger.error(f"睡眠日記取得中にエラー: {str(e)}")
        flash(f"エラーが発生しました: {str(e)}", 'error')
        return redirect(url_for('home'))

# 睡眠日記の追加
@app.route('/add_sleep_diary', methods=['GET', 'POST'])
@login_required
def add_sleep_diary():
    if request.method == 'POST':
        # フォームのデータを取得
        date = request.form.get('date')
        sleep_quality = request.form.get('sleep_quality')
        memo = request.form.get('memo')

        # 必須項目のチェック
        if not date or not sleep_quality:
            flash('日付と睡眠の質は必須項目です。', 'error')
            return redirect(url_for('add_sleep_diary'))  # フォームを再表示

        try:
            # 日記の作成
            with SessionLocal() as session_db:
                create_sleep_diary(session_db, current_user.id, date, sleep_quality, memo)
                flash('睡眠日記を追加しました！', 'success')
                return redirect(url_for('sleep_diary_list'))  # 日記リストにリダイレクト
        except Exception as e:
            app.logger.error(f"睡眠日記追加中にエラー: {str(e)}")
            flash(f"エラーが発生しました: {str(e)}", 'error')

    return render_template('add_sleep_diary.html')  # 新しい日記を追加するフォームを返す

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
