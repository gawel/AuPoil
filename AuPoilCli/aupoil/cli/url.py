# -*- coding: utf-8 -*-
from paste.proxy import Proxy
from urlparse import urlparse
from webob import Request
import simplejson
import re

valid_schemes = set(['http', 'https', 'ftp'])
_re_alias = re.compile('^[A-Za-z0-9-_.]{1,}$')

def add(url, alias=None, server='http://a.pwal.fr'):
    parsed = urlparse(url)
    scheme = parsed[0]
    netloc = parsed[1]
    if scheme not in valid_schemes:
        print 'You must provide a valid url. Supported schemes are %s' % ', '.join(valid_schemes)
        return
    elif not netloc:
        print 'You must provide a valid url.'
        return

    if alias and not _re_alias.match(alias):
        print 'Invalid alias. Valid chars are A-Za-z0-9-_.'
        return

    app = Proxy(server)
    req = Request.blank('/json')
    qs = 'url=%s' % url
    if alias:
        qs += '&alias=%s' % alias
    req.environ['QUERY_STRING'] = qs
    resp = req.get_response(app)
    if resp.content_type.startswith('text/javascript'):
        try:
            return simplejson.loads(resp.body)
        except ValueError:
            raise ValueError(resp.body)
    return dict(code=1, error='Server error')

def stats(url, alias=None, server='http://a.pwal.fr'):
    app = Proxy(server)
    req = Request.blank('/json/stats')
    qs = 'url=%s' % url
    if alias:
        qs += '&alias=%s' % alias
    req.environ['QUERY_STRING'] = qs
    resp = req.get_response(app)
    if resp.content_type.startswith('text/javascript'):
        try:
            return simplejson.loads(resp.body)
        except ValueError:
            raise ValueError(resp.body)
    return dict(code=1, error='Server error')

