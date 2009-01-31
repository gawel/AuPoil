# -*- coding: utf-8 -*-
import sqlalchemy as sa
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


