# -*- coding: utf-8 -*-
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
__all__ = []
engine = None
metadata = MetaData()
Base = declarative_base(metadata=metadata)
Session = None


