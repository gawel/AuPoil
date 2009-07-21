from mako.lookup import TemplateLookup
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import exc as saexc
from paste.request import resolve_relative_url
from webob import Request, Response, exc
from urlparse import urlparse
from aupoil.model import Url, Stat
from aupoil import meta
import simplejson
import urllib
import random
import string
import re
import os

dirname = os.path.dirname(__file__)

_re_alias = re.compile('^[A-Za-z0-9-_.]{1,}$')

valid_chars = string.digits+string.ascii_letters

sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=meta.engine)

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
        self.stats = self.templates.get_template('/stats.mako')

    def random_alias(self, min_max=[4, 6]):
        chars = [s for s in valid_chars]
        random.shuffle(chars)
        return ''.join(random.sample(chars, random.randint(*min_max)))

    def add(self, environ, url, alias=None):
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

        if alias and not _re_alias.match(alias):
            c.error = 'Invalid alias. Valid chars are A-Za-z0-9-_.'
            return c

        host = resolve_relative_url('/', environ)
        if host.endswith('/'):
            host = host[:-1]

        if url.startswith(host):
            c.error = 'This is not very useful. right ?'
            return c

        if alias:
            id = alias
        else:
            for i in [1,2,3]:
                id = self.random_alias([5,10])
                record = meta.engine.execute(sa.select([Url.alias], Url.alias==id)).fetchone()
                if record is None:
                    break

        c.code = 0

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
                record = meta.engine.execute(sa.select([Url.alias, Url.url], sa.or_(Url.url==url, Url.alias==id))).fetchone()
            else:
                record = meta.engine.execute(sa.select([Url.alias, Url.url], Url.url==url)).fetchone()
            if url:
                old_alias = record[0]
                old_url = record[1]
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
            c.new_url = '%s/%s' % (host, id)
        if c.error:
            c.error = str(c.error)
        Session.remove()
        return c

    def get_stats(self, alias):
        query = sa.select([Stat.alias, Stat.referer, sa.func.count(Stat.referer)],
                          Stat.alias==alias, group_by=Stat.referer)
        results = meta.engine.execute(query).fetchall()
        results = [dict(referer=i[1], count=i[2]) for i in results]
        results.sort(cmp=lambda a, b: cmp(a['count'], b['count']))
        total = 0
        for item in results:
            total += item.get('count', 0)
        results.append(dict(referer='Total', count=total))
        return results

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO')[1:]
        if path_info.startswith('json'):
            req = Request(environ)
            resp = Response()
            resp.content_type = 'text/javascript'
            resp.charset = 'utf-8'
            callback = req.GET.get('callback')
            alias = req.GET.get('alias')
            url = req.GET.get('url')
            if path_info.startswith('json/stats'):
                if alias:
                    Session = orm.scoped_session(sm)
                    url = Session.query(Url).get(alias)
                    c = Params(url=url.url, alias=url.alias, stats=self.get_stats(alias))
                    Session.close()
                else:
                    c = Params(error='You must provide an alias !')
            else:
                if url:
                    c = self.add(environ, url, alias)
                else:
                    c = Params(error='You must provide an url !')
            if callback:
                resp.body = '%s(%s);' % (callback, simplejson.dumps(c))
            else:
                resp.body = simplejson.dumps(c)
        elif path_info.startswith('stats'):
            resp = Response()
            Session = orm.scoped_session(sm)
            dirnames = path_info.split('/')
            if len(dirnames) > 1:
                alias = dirnames[-1]
                query = sa.select([Stat.alias, Stat.referer, sa.func.count(Stat.referer)],
                                  Stat.alias==alias, group_by=Stat.referer)
                c = Params(url=Session.query(Url).get(alias),
                           results=self.get_stats(alias))
                resp.body = self.stats.render(c=c)
        elif path_info:
            # redirect
            Session = orm.scoped_session(sm)

            alias = path_info.split('/')[0]
            url = Session.query(Url).get(alias)
            if url is not None:
                if environ.get('REQUEST_METHOD', 'GET').lower() in ('get', 'post'):
                    record = Stat()
                    record.alias = alias
                    record.referer = environ.get('HTTP_REFERER', 'UNKOWN')
                    Session.add(record)
                    Session.commit()
                resp = exc.HTTPFound(location=str(url.url))
            else:
                resp = exc.HTTPNotFound('This url does not exist')
            Session.remove()
        else:
            resp = Response()
            req = Request(environ)
            resp.content_type = 'text/html'
            resp.charset = 'utf-8'
            if req.GET.get('url'):
                # save
                alias = req.GET.get('alias')
                alias = alias and alias or None
                url = req.GET.get('url')
                if url:
                    c = self.add(environ, url, alias)
                else:
                    c = Params(error='You must provide an url !')
            else:
                c = Params(url=req.GET.get('post',''))
            c.plugin = req.GET.get('p', False)
            resp.body = self.index.render(c=c)
        return resp(environ, start_response)


