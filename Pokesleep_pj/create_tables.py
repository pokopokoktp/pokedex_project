# -*- coding: utf-8 -*-

from database import Base, engine
import models  

# 既存のテーブルは維持され、新しいテーブルだけ作成される
Base.metadata.create_all(engine)
