from mako.lookup import TemplateLookup
from sqlalchemy import orm
from sqlalchemy import exc as saexc
from paste.request import resolve_relative_url
from webob import Request, Response, exc
from urlparse import urlparse
from aupoil.model import Url
from aupoil import meta
import random
import string
import re
import os

dirname = os.path.dirname(__file__)

_re_alias = re.compile('^[A-Za-z0-9-_.]{1,}$')

class Params(dict):
    def __getattr__(self, attr):
        return self.get(attr, '')
    def __setattr__(self, attr, value):
        self[attr] = value

class AuPoilApp(object):

    def __init__(self, debug=False, **conf):
        self.valid_schemes = set(['http', 'https', 'ftp'])
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
        if not url:
            c.error = 'You must provide an url'
            return c

        parsed = urlparse(url)
        if parsed.scheme not in self.valid_schemes:
            c.error = 'You must provide a valid url. Supported schemes are %s' % ', '.join(self.valid_schemes)
            return c
        elif not parsed.netloc:
            c.error = 'You must provide a valid url.'
            return c

        if alias and not _re_alias.match(alias):
            c.error = 'Invalid alias. Valid chars are A-Za-z0-9-_.'
            return c

        c.code = 0

        id = alias is not None and alias or self.random_alias
        assert id is not None
        sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=meta.engine)
        Session = orm.scoped_session(sm)
        record = Url()
        record.alias = id
        record.url = url
        Session.add(record)
        try:
            Session.commit()
        except saexc.IntegrityError:
            c.code = 1
            if alias:
                c.error = 'This alias already exist'
            else:
                c.error = 'An error occur'
        else:
            c.url = url
            c.new_url = resolve_relative_url('/%s' % id, environ)
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
        elif path_info:
            # redirect
            alias = path_info.split('/')[0]
            url = meta.engine.execute(Url.__table__.select(Url.alias==alias)).fetchone()
            if url:
                resp = exc.HTTPFound(location=str(url[1]))
            else:
                resp = exc.HTTPNotFound('This url does not exist')
        else:
            resp = Response()
            resp.content_type = 'text/html'
            resp.charset = 'utf-8'
            if meth == 'GET' and 'url=' in environ.get('QUERY_STRING'):
                # save
                req = Request(environ)
                alias = req.GET.get('alias')
                url = req.GET.get('url')
                if url:
                    c = self.add(environ, url, alias)
                else:
                    c = Params(error='You must provide an url !')
            else:
                c = Params()
            resp.body = self.index.render(c=c)
        return resp(environ, start_response)


