# -*- coding: utf-8 -*-
from optparse import OptionParser
from paste.urlmap import URLMap
from paste.script.appinstall import Installer
from paste.urlparser import StaticURLParser
from sqlalchemy import engine_from_config
from sqlalchemy import orm
from aupoil import meta
from aupoil import model
import os

class AuPoilInstaller(Installer):
    pass

def make_app(global_conf, **conf):
    engine = engine_from_config(conf, 'sqlalchemy.')
    meta.engine = engine
    meta.metadata.bind = engine
    meta.Session = orm.sessionmaker(autoflush=True, autocommit=False, bind=meta.engine)
    from aupoil.application import AuPoilApp
    app = AuPoilApp(**conf)
    if 'templates_path' in conf:
        map = URLMap()
        map['/_static'] = StaticURLParser(conf['templates_path'])
        map['/'] = app
        return map
    return app

def main():
    parser = OptionParser()
    parser.add_option("-l", "--latest", dest="latest",
                      action="count", help="show latest entries")
    parser.add_option("-d", "--delete", dest="delete",
                      default=None, help="delete alias")
    (options, args) = parser.parse_args()
    from paste.deploy import loadapp
    wsgi_app = loadapp('config:%s' % os.path.join(os.getcwd(), args[0]))
    Session = meta.Session()
    if options.delete:
        url = Session.query(model.Url).get(options.delete)
        if url:
            for stat in url.stats:
                Session.delete(stat)
            Session.delete(url)
            Session.commit()
    if options.latest:
        for url in Session.query(model.Url).order_by(model.Url.date.desc()).limit(options.latest*20).all():
            print repr(url)
