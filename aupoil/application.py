from sqlalchemy import engine_from_config
from mako.lookup import TemplateLookup
from paste.deploy import CONFIG
from webob import Request, Response, exc
from aupoil import meta

dirname = os.path.dirname(__file__)

class Params(dict):
    def __getattr__(self, attr):
        return self.get(attr, '')
    def __setattr__(self, attr, value):
        self[attr] = value

class AuPoilApp(object):
    def __init__(self, **conf):
        self.title = conf['title']
        self.templates = TemplateLookup(
                            directories=[dirname],
                            output_encoding='utf8',
                            default_filters=['decode.utf8'])
        self.index = self.templates.get_template('/index.mako')

    @property
    def Session(self):
        sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=meta.engine)
        return orm.scoped_session(sm)

    def __init__(environ, start_response):
        path_info = environ.get('PATH_INFO')
        meth = environ.get('REQUEST_METHOD')
        if path_info:
            if path_info.startswith('/api'):
                # api
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
                alias = alias and alias or random_alias()
                Session = self.Session
                Session.add(Url(alias=alias, url=url))
                Session.commit()
                host = req.script_name and '%s/%s' (self.host, req.script_name) or self.host
                c.url = 'http://%s/%s' % (host, alias)
        resp.unicode_body = self.index.render(c=c)
        return resp(environ, start_response)


