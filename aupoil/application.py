from paste.request import resolve_relative_url
from mako.lookup import TemplateLookup
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import exc as saexc
from webob import Request, Response, exc
from aupoil import meta
from aupoil.model import Url
from aupoil.model import Stat
from aupoil.utils import Params
from aupoil.utils import session
from aupoil.utils import valid_chars
from aupoil.utils import random_alias
from urlparse import urlparse
import simplejson
import urllib
import re
import os

dirname = os.path.dirname(__file__)

_re_alias = re.compile('^[A-Za-z0-9-_.]{1,}$')


@session
def get_stats(alias, Session=None):
    if isinstance(alias, str):
        alias = alias.decode('utf-8')
    url = Session.query(Url).get(alias)
    query = sa.select([Stat.alias, Stat.referer, sa.func.count(Stat.referer)],
                      Stat.alias==alias, group_by=Stat.referer)
    results = Session.execute(query).fetchall()
    results = [dict(referer=i[1], count=i[2]) for i in results]
    results.sort(cmp=lambda a, b: cmp(a['count'], b['count']))
    total = 0
    for item in results:
        total += item.get('count', 0)
    c = Params(url=url.url, alias=url.alias, count=total, stats=results)
    return c


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

    @session
    def add(self, req, url=None, alias=None, Session=None):
        c = Params(code=1)
        if not url:
            c.error = 'You must provide an url'
            return c

        if len(url) > 255:
            c.error = 'Lamer !'
            return c

        parsed = urlparse(url)
        scheme = parsed[0]
        netloc = parsed[1]
        if scheme not in self.valid_schemes:
            c.error = 'You must provide a valid url. Supported schemes are %s' % ', '.join(self.valid_schemes)
            return c
        elif not netloc or [a for a in netloc if a not in valid_chars + '._-']:
            c.error = 'You must provide a valid url.'
            return c

        fragment = qs = ''
        if '#' in url:
            url, fragment = url.split('#', 1)
            fragment = '#%s' % fragment
        if '?' in url:
            url, qs = url.split('?', 1)
            qs = '?%s' % qs

        host = '%s://%s' % (scheme, netloc)
        url = url[len(host):]
        url = '%s%s%s%s' % (host, urllib.quote(url), qs, fragment)

        host = resolve_relative_url('/', req.environ)
        if host.endswith('/'):
            host = host[:-1]

        if url.startswith(host):
            c.error = 'This is not very useful. right ?'
            return c

        if isinstance(url, str):
            url = url.decode('utf-8')

        if isinstance(alias, str):
            alias = alias.decode('utf-8')

        if alias:
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
                    c.error = '%s is already bind to %s/%s' % (url, host, old_alias)
                    c.new_url = '%s/%s' % (host, old_alias)
                elif old_alias == alias:
                    c.error = '%s/%s is already bind to %s' % (host, alias, old_url)
                else:
                    c.error = str(url)
            elif alias:
                c.error = 'This alias already exist'
            else:
                c.error = 'An error occur'
        else:
            c.url = url
            c.new_url = u'%s/%s' % (host, id)
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

        callback = req.params.get('callback')
        if callback:
            resp.body = '%s(%s);' % (callback, simplejson.dumps(c))
        else:
            resp.body = simplejson.dumps(c)
        return resp

    @session
    def redirect(self, req, Session=None):
        path_info = req.path_info.strip('/')
        alias = path_info.decode('utf-8')
        url = Session.query(Url).get(alias)
        if url is not None:
            if req.method.lower() == 'get':
                record = Stat()
                record.alias = alias
                record.referer = req.environ.get('HTTP_REFERER', 'UNKOWN').decode('utf-8')
                Session.add(record)
                Session.commit()
            resp = exc.HTTPFound(location=str(url.url))
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
        elif path_info:
            resp = self.redirect(req)
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
            c.plugin = req.GET.get('p', False)
            resp.body = self.index.render(c=c)
        return resp(environ, start_response)


