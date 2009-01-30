from mako.lookup import TemplateLookup
from sqlalchemy import orm
from sqlalchemy import exc as saexc
from paste.request import resolve_relative_url
from webob import Request, Response, exc
from aupoil.model import Url
from aupoil import meta
import random
import string
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
    def random_alias(self):
        chars = [s for s in string.digits+string.ascii_letters]
        random.shuffle(chars)
        return ''.join(random.sample(chars, 10))

    def add(self, environ, url, alias=None):
        c = Params(code=1)
        id = alias and alias or self.random_alias
        sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=meta.engine)
        Session = orm.scoped_session(sm)
        record = Url()
        record.alias = id
        record.url = url
        Session.add(record)
        try:
            Session.commit()
        except saexc.IntegrityError:
            c.code = 0
            if alias:
                c.error = 'This alias already exist'
            else:
                c.error = 'An error occur'
        else:
            c.new_url = resolve_relative_url('/%s' % alias, environ)
        Session.remove()
        return c

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO')[1:]
        meth = environ.get('REQUEST_METHOD')
        if meth == 'PUT':
            req = Request(environ)
            resp = Response()
            resp.content_type = 'text/javascript'
            resp.charset = 'utf-8'
            alias = path_info and path_info.split('/')[0] or None
            c = self.add(environ, req.body.strip(), alias)
            resp.body = repr(c)
        elif path_info and meth == 'GET':
            # redirect
            alias = path_info.split('/')[0]
            url = meta.engine.execute(Url.__table__.select(Url.alias==alias))
            resp = exc.HTTPFound(location='http://www.gawel.org')
        else:
            resp = Response()
            resp.content_type = 'text/html'
            resp.charset = 'utf-8'
            if meth == 'POST':
                # save
                req = Request(environ)
                alias = req.POST.get('alias')
                url = req.POST.get('url')
                if url:
                    c = self.add(environ, url, alias)
                else:
                    c = Params(error='You must provide an url !')
            else:
                c = Params()
            resp.body = self.index.render(c=c)
        return resp(environ, start_response)


