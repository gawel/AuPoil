# -*- coding: utf-8 -*-
import sqlalchemy as sa
from sqlalchemy import orm
from aupoil import meta
from datetime import datetime

class Url(meta.Base):
    __tablename__ = 'urls'
    alias = sa.Column('alias', sa.Unicode(25), primary_key=True)
    url = sa.Column('url', sa.Unicode(255), index=True, unique=True)
    date = sa.Column('date', sa.DateTime, default=datetime.now)
    frame = sa.Column('frame', sa.Boolean, default=False)
    zip = sa.Column('zip', sa.Boolean, default=False)
    ip = sa.Column('ip', sa.String(64))

    def __repr__(self):
        return '%-3s %-30r %r' % (len(self.stats), self.alias , self.url[:80])

    def __str__(self):
        return self.url.encode('utf-8')

class Stat(meta.Base):
    __tablename__ = 'stats'
    id = sa.Column('id', sa.Integer, primary_key=True)
    referer = sa.Column('referer', sa.Unicode(255), default='UNKOWN')
    alias = sa.Column('alias', sa.ForeignKey('urls.alias'))
    url = orm.relation(Url, uselist=False, backref='stats')

