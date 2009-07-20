# -*- coding: utf-8 -*-
import sqlalchemy as sa
from sqlalchemy import orm
from aupoil import meta
from datetime import datetime

class Url(meta.Base):
    __tablename__ = 'urls'
    alias = sa.Column('alias', sa.String(25), primary_key=True)
    url = sa.Column('url', sa.String(255), index=True, unique=True)
    date = sa.Column('date', sa.DateTime, default=datetime.now)
    frame = sa.Column('frame', sa.Boolean, default=False)
    zip = sa.Column('zip', sa.Boolean, default=False)
    ip = sa.Column('ip', sa.String(64))

class Stat(meta.Base):
    __tablename__ = 'counters'
    id = sa.Column('id', sa.Integer, primary_key=True)
    referer = sa.Column('referer', sa.String(255), default='UNKOWN')
    alias = sa.Column('alias', sa.ForeignKey('urls.alias'))
    url = orm.relation(Url, uselist=False)

