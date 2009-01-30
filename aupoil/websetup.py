# -*- coding: utf-8 -*-
from sqlalchemy import engine_from_config
from aupoil import meta
from aupoil import model

def setup_app(command, conf, vars):
    engine = engine_from_config(conf, 'sqlalchemy.')
    meta.engine = engine
    meta.metadata.bind = engine
    meta.metadata.create_all(checkfirst=True)

