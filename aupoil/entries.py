# -*- coding: utf-8 -*-
from paste.urlmap import URLMap
from paste.script.appinstall import Installer
from paste.urlparser import StaticURLParser
from sqlalchemy import engine_from_config
from aupoil import meta
from aupoil import model

class AuPoilInstaller(Installer):
    pass

def make_app(global_conf, **conf):
    engine = engine_from_config(conf, 'sqlalchemy.')
    meta.engine = engine
    meta.metadata.bind = engine
    from aupoil.application import AuPoilApp
    app = AuPoilApp(**conf)
    if 'templates_path' in conf:
        map = URLMap()
        map['/_static'] = StaticURLParser(conf['templates_path'])
        map['/'] = app
        return map
    return app
