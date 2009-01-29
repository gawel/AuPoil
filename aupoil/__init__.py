#
from aupoil import meta
from aupoil import model

def make_app(global_conf, **local_conf):
    meta.engine = engine_from_config(conf, 'sqlalchemy.')
    meta.engine = engine
    meta.metadata.bind = engine
    meta.metadata.create_all(checkfirst=True)
    from aupoil.application import AuPoilApp
    return AuPoilApp(**local_conf)
