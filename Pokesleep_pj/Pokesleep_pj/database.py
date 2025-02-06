from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# エンジンの作成
engine = create_engine('postgresql+psycopg2://pokesleep_user:pokemonzukan@localhost/pokesleep_db')

# Baseを一度だけ定義し、それを使用
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pokemon, User, UserPokemon, SleepDiaryの定義はmodels.pyで行っているのでここでは省略
