# -*- coding: utf-8 -*-
import sqlalchemy as sa
from aupoil import meta
from datetime import datetime

class Urls(meta.Base):
    __tablename__ = 'urls'
    alias = sa.Column('alias', sa.String(25), primary_key=True)
    url = sa.Column('url', sa.String(255))
    date = sa.Column('date', sa.DateTime, default=datetime.now)
    ip = sa.Column('ip', sa.String(15))


