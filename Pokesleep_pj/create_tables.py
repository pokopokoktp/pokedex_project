# -*- coding: utf-8 -*-

from database import Base, engine
import models  

# �����̃e�[�u���͈ێ�����A�V�����e�[�u�������쐬�����
Base.metadata.create_all(engine)
