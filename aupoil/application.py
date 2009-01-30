from mako.lookup import TemplateLookup
from sqlalchemy import orm
from sqlalchemy import exc as saexc
from paste.request import resolve_relative_url
from webob import Request, Response, exc
from aupoil.model import Url
from aupoil import meta
import os

dirname = os.path.dirname(__file__)

class Params(dict):
    def __getattr__(self, attr):
        return self.get(attr, '')
    def __setattr__(self, attr, value):
        self[attr] = value

class AuPoilApp(object):

    def __init__(self, title='', debug=False, **conf):
        self.title = title
        self.debug = debug in ('true', True)
        directories = [dirname]
        if 'templates_path' in conf:
            directories.insert(0, conf['templates_path'])
        self.templates = TemplateLookup(
                            directories=directories,
                            output_encoding='utf8',
                            default_filters=['decode.utf8'])
        self.index = self.templates.get_template('/index.mako')

    @property
    def Session(self):
        sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=meta.engine)
        return orm.scoped_session(sm)

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO')[1:]
        meth = environ.get('REQUEST_METHOD')
        if path_info:
            if path_info.startswith('api'):
                # api
                pass
            elif meth == 'GET':
                # redirect
                alias = path_info.split('/')[0]
                url = meta.engine.execute(Url.__table__.select(alias=alias))
                exc.HTTPFound(location='http://www.gawel.org')
        resp = Response()
        resp.content_type = 'text/html'
        resp.charset = 'utf-8'
        c = Params(title=self.title)
        if meth == 'POST':
            # save
            req = Request(environ)
            alias = req.POST.get('alias')
            url = req.POST.get('url')
            if url:
                id = alias and alias or random_alias()
                Session = self.Session
                record = Url()
                record.alias = id
                record.url = url
                Session.add(record)
                try:
                    Session.commit()
                except saexc.IntegrityError:
                    pass
                c.url = resolve_relative_url('/%s' % alias, environ)
        resp.body = self.index.render(c=c)
        return resp(environ, start_response)


