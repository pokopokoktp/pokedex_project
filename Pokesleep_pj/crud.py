from sqlalchemy.orm import Session
from models import User, Pokemon, UserPokemon, SleepDiary
from werkzeug.security import generate_password_hash

# ユーザーの追加
def create_user(session, username, hashed_password):
    new_user = User(username=username, password=hashed_password)
    session.add(new_user)
    session.commit()


# ポケモンの追加
def create_pokemon(session_db, name, number, sleep_type, specialty, main_skill):
    try:
        # 新しいポケモンの作成
        new_pokemon = Pokemon(
            name=name,
            number=number,  # 手動で設定された番号
            sleep_type=sleep_type,
            specialty=specialty,
            main_skill=main_skill
        )
        session_db.add(new_pokemon)
        session_db.commit()  # コミットしてデータベースに保存
        print(f"ポケモン {name} を追加しました (番号: {number})")  # デバッグ用
    except Exception as e:
        print(f"ポケモン追加エラー: {e}")  # エラーメッセージ
        raise e




# ポケモンの一覧取得
def get_pokemon_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pokemon).offset(skip).limit(limit).all()

# ユーザーが獲得したポケモンの追加
def catch_pokemon(db: Session, user_id: int, pokemon_id: int):
    # ユーザーとポケモンの関連付け
    user_pokemon = UserPokemon(user_id=user_id, pokemon_id=pokemon_id)
    db.add(user_pokemon)
    db.commit()
    db.refresh(user_pokemon)

    return user_pokemon

# ユーザーの睡眠日記を追加
def create_sleep_diary(db: Session, user_id: int, date: str, sleep_quality: str, memo: str):
    sleep_diary = SleepDiary(user_id=user_id, date=date, sleep_quality=sleep_quality, memo=memo)
    db.add(sleep_diary)
    db.commit()
    db.refresh(sleep_diary)
    return sleep_diary

# ユーザーが獲得したポケモンのリストを取得
def get_user_pokemons(db: Session, user_id: int):
    # UserPokemon と Pokemon を結びつけて、ポケモン情報も取得する
    return db.query(Pokemon).join(UserPokemon).filter(UserPokemon.user_id == user_id).all()

