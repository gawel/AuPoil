# -*- coding: utf-8 -*-
from sqlalchemy import orm
from aupoil import meta
import random
import string

valid_chars = string.digits+string.ascii_letters+':'
valid_unicode = [unicode(c, 'utf-8') for c in valid_chars]

def random_alias(min_max=[4, 6]):
    chars = [s for s in valid_unicode]
    random.shuffle(chars)
    return u''.join(random.sample(chars, random.randint(*min_max)))

def session(func):
    def wrapper(*args, **kwargs):
        Session = meta.Session()
        kwargs['Session'] = Session
        try:
            value = func(*args, **kwargs)
        finally:
            Session.close()
        return value
    return wrapper

class Params(dict):
    def __getattr__(self, attr):
        return self.get(attr, '')
    def __setattr__(self, attr, value):
        self[attr] = value


