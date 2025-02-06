# -*- coding: utf-8 -*- 
from flask import Flask, request, render_template, redirect, url_for, session, flash 
from flask_login import LoginManager, login_user, login_required, logout_user, current_user 
from flask_migrate import Migrate 
from werkzeug.security import generate_password_hash, check_password_hash 
from models import User, Pokemon, UserPokemon, SleepDiary, db  # インポートパス修正
from crud import create_user, create_pokemon, get_pokemon_list, catch_pokemon, create_sleep_diary, get_user_pokemons
from database import SessionLocal, engine 

app = Flask(__name__)

# ✅ 固定のシークレットキー（デバッグしやすい） 
app.secret_key = 'your_secret_key'  # 固定キーでOK。os.urandomは削除。

# DBマイグレーション
migrate = Migrate(app, engine)

# Flask-Login の初期化
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ユーザーをロードする関数
@login_manager.user_loader
def load_user(user_id):
    try:
        with SessionLocal() as session_db:
            user = session_db.query(User).get(int(user_id))
        return user
    except Exception as e:
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

        session_db = SessionLocal()
        user = session_db.query(User).filter(User.username == username).first()

        if user and user.check_password(password):  # 修正
            login_user(user)
            session_db.close()
            flash('ログインに成功しました！')
            return redirect(url_for('home'))
        else:
            flash('ユーザー名またはパスワードが正しくありません')

        session_db.close()

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
            caught_pokemon_ids = [up.id for up in user_pokemons]  # user_pokemons の ID を取得

            # ユーザーが獲得したポケモンの名前をリストとして取得
            user_pokemon_names = [pokemon.name for pokemon in user_pokemons]
            
            print(f"全ポケモン: {[pokemon.name for pokemon in pokemons]}")
            print(f"ユーザーが獲得したポケモン: {user_pokemon_names}")
            
        return render_template('pokemon_list.html', pokemons=pokemons, caught_pokemon_ids=caught_pokemon_ids)
    except Exception as e:
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
        return redirect(url_for('pokemon_list'))  # ポケモン一覧にリダイレクト
    except Exception as e:
        flash(f"ポケモンを獲得できませんでした: {str(e)}", 'error')
        return redirect(url_for('pokemon_list'))

# 管理者専用のデコレーター
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash("管理者権限が必要です。", 'error')
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/add_pokemon', methods=['GET', 'POST'])
@admin_required  # 管理者専用のデコレーター
def add_pokemon():
    if request.method == 'POST':
        # フォームデータの取得
        name = request.form['name']
        number = int(request.form['number'])  # 手動で入力された番号
        sleep_type = request.form['sleep_type']
        specialty = request.form['specialty']
        main_skill = request.form['main_skill']

        # バリデーション: すべてのフィールドが入力されているかをチェック
        if not name or not sleep_type or not specialty or not main_skill or not number:
            flash('すべてのフィールドを入力してください。', 'error')
            return render_template('add_pokemon.html')  # エラーメッセージとともに再表示

        # データベース接続
        session_db = SessionLocal()

        try:
            # ポケモンを追加
            create_pokemon(session_db, name, number, sleep_type, specialty, main_skill)
            flash('ポケモンを追加しました！')
            session_db.commit()  # コミットして変更を保存
        except Exception as e:
            flash(f"エラーが発生しました: {str(e)}", 'error')
        finally:
            session_db.close()  # セッションを閉じる

        return redirect(url_for('pokemon_list'))  # ポケモンリストにリダイレクト

    return render_template('add_pokemon.html')  # 管理者用のポケモン追加フォーム

# ユーザー登録機能
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='scrypt', salt_length=16)

        session_db = SessionLocal()
        if session_db.query(User).filter(User.username == username).first():
            flash('すでに存在するユーザー名です。')
        else:
            create_user(session_db, username, hashed_password)
            flash('ユーザー登録が完了しました！')
            session_db.close()
            return redirect(url_for('login'))

        session_db.close()

    return render_template('register.html')

# 睡眠日記の表示
@app.route('/view_diaries')
@login_required
def view_diaries():
    try:
        with SessionLocal() as session_db:
            diaries = session_db.query(SleepDiary).filter(SleepDiary.user_id == current_user.id).all()
        return render_template('sleep_diary_list.html', diaries=diaries)
    except Exception as e:
        flash(f"エラーが発生しました: {str(e)}", 'error')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
