# -*- coding: utf-8 -*-
from sqlalchemy import orm
from aupoil import meta
import random
import string

sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=meta.engine)

valid_chars = string.digits+string.ascii_letters

def random_alias(min_max=[4, 6]):
    chars = [s for s in valid_chars]
    random.shuffle(chars)
    return ''.join(random.sample(chars, random.randint(*min_max)))

def session(func):
    def wrapper(*args, **kwargs):
        Session = orm.scoped_session(sm)
        kwargs['Session'] = Session
        try:
            value = func(*args, **kwargs)
        finally:
            Session.remove()
        return value
    return wrapper

class Params(dict):
    def __getattr__(self, attr):
        return self.get(attr, '')
    def __setattr__(self, attr, value):
        self[attr] = value


