from paste.request import resolve_relative_url
from mako.lookup import TemplateLookup
import sqlalchemy as sa
from sqlalchemy import orm
try:
    from sqlalchemy import exc as saexc
except ImportError:
    from sqlalchemy import exceptions as saexc
from webob import Request, Response, exc
from aupoil import meta
from aupoil.model import Url
from aupoil.model import Stat
from aupoil.utils import Params
from aupoil.utils import session
from aupoil.utils import valid_chars
from aupoil.utils import random_alias
from urlparse import urlparse
import urllib
import os

try:
    import json
except ImportError:
    import simplejson as json

dirname = os.path.dirname(__file__)

@session
def get_stats(alias, Session=None):
    if isinstance(alias, str):
        alias = alias.decode('utf-8')

    url = Session.query(Url).get(alias)
    if url is None:
        return Params(error='Not found', alias=alias, count=0, stats=[])

    query = sa.select([Stat.alias, Stat.referer, sa.func.count(Stat.referer)],
                      Stat.alias==alias, group_by=Stat.referer)
    results = Session.execute(query).fetchall()
    results = [dict(referer=i[1], count=i[2]) for i in results]
    results.sort(cmp=lambda a, b: cmp(a['count'], b['count']))

    total = 0
    for item in results:
        total += item.get('count', 0)

    return Params(url=url.url, alias=url.alias, count=total, stats=results)


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
        self.stats = self.templates.get_template('/stats.mako')
        self.redirect_url = conf.get('redirect_url', None)
        self.stats_on = conf.get('stats', 'on') == 'on'

    @session
    def add(self, req, url=None, alias=None, Session=None):
        c = Params(code=1)
        if not url:
            c.error = 'You must provide an url'
            return c

        if len(url) > 255:
            c.error = 'Lamer !'
            return c

        scheme, netloc, path_info, dummy, qs, fragment = urlparse(url)
        if scheme not in self.valid_schemes:
            c.error = 'You must provide a valid url. Supported schemes are %s' % ', '.join(self.valid_schemes)
            return c
        elif not netloc or [a for a in netloc if a not in valid_chars + '._-']:
            c.error = 'You must provide a valid url.'
            return c

        my_host = resolve_relative_url('/', req.environ)
        if my_host.endswith('/'):
            my_host = my_host[:-1]

        if url.startswith(my_host):
            c.error = 'This is not very useful. right ?'
            return c

        #url = url.replace(' ', '%20')
        if isinstance(url, str):
            url = url.decode('utf-8')

        if alias:
            for char in '\?& ':
                alias = alias.replace(char, '-')
            if isinstance(alias, str):
                alias = alias.decode('utf-8')
            id = alias
        else:
            for i in [1,2,3]:
                id = random_alias([5,10])
                record = Session.execute(sa.select([Url.alias], Url.alias==id)).fetchone()
                if record is None:
                    break

        c.code = 0

        record = Url()
        record.alias = id
        record.url = url
        Session.add(record)
        try:
            Session.commit()
        except saexc.IntegrityError:
            c.code = 1
            if alias:
                record = meta.engine.execute(sa.select([Url.alias, Url.url], sa.or_(Url.url==url, Url.alias==id))).fetchone()
            else:
                record = meta.engine.execute(sa.select([Url.alias, Url.url], Url.url==url)).fetchone()
            if url:
                old_alias = record.alias
                old_url = record.url
                if old_url == url:
                    c.error = '%s is already bind to %s/%s' % (url, my_host, old_alias)
                    c.url = url
                    c.new_url = u'%s/%s' % (my_host, old_alias)
                elif old_alias == alias:
                    c.error = u'%s/%s is already bind to %s' % (my_host, alias, old_url)
                else:
                    c.error = url
            elif alias:
                c.error = 'This alias already exist'
            else:
                c.error = 'An error occur'
        else:
            c.url = url
            c.new_url = u'%s/%s' % (my_host, id)
        if c.error:
            c.error = c.error
        return c

    def json(self, req):
        resp = Response()
        resp.content_type = 'text/javascript'
        resp.charset = 'utf-8'
        alias = req.params.get('alias')
        url = req.params.get('url')

        path_info = req.path_info.lstrip('/')
        if path_info.startswith('json/stats'):
            if alias:
                c = get_stats(alias)
            else:
                c = Params(error='You must provide an alias !')
        else:
            if url:
                c = self.add(req, url, alias)
            else:
                c = Params(error='You must provide an url !')

        callback =req.params.get('callback')
        if callback:
            callback = str(callback)
            arg = req.params.get('arg')
            if arg:
                resp.body = '%s(%s, %s);' % (callback, json.dumps(arg), json.dumps(c))
            else:
                resp.body = '%s(%s);' % (callback, json.dumps(c))
        else:
            resp.body = json.dumps(c)
        return resp

    @session
    def redirect(self, req, Session=None):
        path_info = req.path_info.strip('/')
        try:
            alias = path_info.decode('utf-8')
        except UnicodeDecodeError:
            alias = path_info.decode('iso-8859-1')
        url = Session.query(Url).get(alias)
        if url is not None:
            if req.method.lower() == 'get' and self.stats_on:
                record = Stat()
                record.alias = alias
                record.referer = req.environ.get('HTTP_REFERER', 'UNKOWN').decode('utf-8')
                Session.add(record)
                Session.commit()
            resp = exc.HTTPMovedPermanently(location=url.url.encode('utf-8'))
        else:
            resp = exc.HTTPNotFound('This url does not exist')
        return resp

    def __call__(self, environ, start_response):
        req = Request(environ)
        path_info = req.path_info.lstrip('/')
        if path_info.startswith('json'):
            resp = self.json(req)
        elif path_info.startswith('stats'):
            resp = Response()
            alias = [p for p in path_info.split('/')[1:] if p]
            if alias:
                alias = '/'.join(alias)
                resp.body = self.stats.render(c=get_stats(alias))
        elif path_info and path_info != 'new':
            resp = self.redirect(req)
        elif not path_info and self.redirect_url:
            resp = exc.HTTPFound(location=self.redirect_url)
        else:
            resp = Response()
            resp.content_type = 'text/html'
            resp.charset = 'utf-8'
            if req.GET.get('url'):
                # save
                alias = req.GET.get('alias')
                alias = alias and alias or None
                url = req.GET.get('url')
                if url:
                    c = self.add(req, url, alias)
                else:
                    c = Params(error='You must provide an url !')
            else:
                c = Params(url=req.GET.get('post',''))
                c.title = req.params.get('title', '')
            c.plugin = req.params.get('p', False)
            resp.body = self.index.render(c=c)
        return resp(environ, start_response)


