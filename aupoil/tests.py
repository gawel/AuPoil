# -*- coding: utf-8 -*-
import os
import sys
import pkg_resources
from unittest import TestCase
from webtest import TestApp
import paste.script.appinstall
from paste.script.appinstall import SetupCommand
from paste.deploy import loadapp

here_dir = os.path.dirname(os.path.abspath(__file__))
conf_dir = os.path.dirname(os.path.dirname(here_dir))

sys.path.insert(0, conf_dir)
pkg_resources.working_set.add_entry(conf_dir)
pkg_resources.require('Paste')
pkg_resources.require('PasteScript')

test_db = os.path.join(conf_dir, "AuPoil", "dev.db")
if os.path.isfile(test_db):
    os.remove(test_db)

config = {"__file__":os.path.join(conf_dir, "AuPoil", "test.ini")}

SetupCommand('setup-app').run([config["__file__"]])

class TestBase(TestCase):

    def __init__(self, *args, **kwargs):
        wsgiapp = loadapp("config:%s" % config["__file__"])
        self.app = TestApp(wsgiapp)
        TestCase.__init__(self, *args, **kwargs)

    def test_alias(self):
        resp = self.app.get('/')
        form = resp.forms["aupoil_form"]
        form["url"] = "http://www.gawel.org"
        form["alias"] = "gawel"
        resp = form.submit()
        resp.mustcontain('http://localhost/gawel')

        resp = self.app.get('/gawel')
        assert resp.headers.get('location') == "http://www.gawel.org", resp

    def test_noalias(self):
        resp = self.app.get('/')
        form = resp.forms["aupoil_form"]
        form["url"] = "http://www.gawel.nu/?toto=true"
        resp = form.submit()
        resp.mustcontain('http://localhost/')

        form = resp.forms["aupoil_result_form"]
        alias = form["result"].value.split('/')[-1]
        assert alias is not None, form["result"].value
        resp = self.app.get("/%s" % alias)
        assert resp.headers.get('Location') == "http://www.gawel.nu/?toto=true", resp

    def test_json_alias(self):
        resp = self.app.get('/json?alias=gawél&url=http://www.gawel.uni')
        resp.mustcontain('{"url": "http://www.gawel.uni", "new_url": "http://localhost/gaw\u00e9l", "code": 0}'.encode('utf-8'))

        resp = self.app.get('/json?alias=gawel_get&url=http://www.gawel.get')
        resp.mustcontain('{"url": "http://www.gawel.get", "new_url": "http://localhost/gawel_get", "code": 0}')

        resp = self.app.get('/json?alias=gawel_get&url=http://www.gawel.org')
        resp.mustcontain('{"url": "http://www.gawel.org", "new_url": "http://localhost/gawel", "code": 1,',
                         '"error": "http://www.gawel.org is already bind to http://localhost/gawel"}')

        resp = self.app.get('/json?alias=gawel_get&url=http://www.gawel.get2')
        resp.mustcontain('{"code": 1, "error": "http://localhost/gawel_get is already bind to http://www.gawel.get"}')

    def test_json(self):
        resp = self.app.get('/json?url=http://www.noalias.get')
        resp.mustcontain('{"url": "http://www.noalias.get", "new_url": "http://localhost/','", "code": 0}')

    def test_json_callback(self):
        resp = self.app.get('/json?url=http://www.callback.get&callback=myFunc')
        resp.mustcontain('myFunc({"url": "http://www.callback.get", "new_url": "http://localhost/','", "code": 0});')

        resp = self.app.get('/json?url=http://www.callback_arg.get&callback=myFunc&arg=myid')
        resp.mustcontain('myFunc("myid", {"url": "http://www.callback_arg.get", "new_url": "http://localhost/','", "code": 0});')

    def test_invalid_url(self):
        resp = self.app.get('/json?url=www.gawel.org')
        resp.mustcontain('You must provide a valid url')

        resp = self.app.get('/json?url=ssh://www.gawel.org')
        resp.mustcontain('You must provide a valid url')

        resp = self.app.get('/json?url=http:/www.gawel.org')
        resp.mustcontain('You must provide a valid url')

    def test_unicode(self):
        resp = self.app.get('/json?url=http://www.gawel.uni/Résultat&alias=')
        resp.mustcontain('{"url": "http://www.gawel.uni/R\u00e9sultat", "new_url": "http://localhost/', '", "code": 0}')
        resp = self.app.get('/json?url=http://www.gawel.uni/Ré&alias=')
        resp.mustcontain('{"url": "http://www.gawel.uni/R\u00e9", "new_url": "http://localhost/', '", "code": 0}')

    def test_longurl(self):
        resp = self.app.get('/json?url=http://www.gawel.uni/Résultat'+255*'-')
        resp.mustcontain('{"code": 1, "error": "Lamer !"}')

    def test_stats(self):
        self.app.get('/json?alias=gawel_get&url=http://www.gawel.get')
        self.app.get('/gawel_get', extra_environ={'HTTP_REFERER':'http://referer0.com'})
        self.app.get('/gawel_get', extra_environ={'HTTP_REFERER':'http://referer0.com'})
        self.app.get('/gawel_get', extra_environ={'HTTP_REFERER':'http://referer1.com'})
        resp = self.app.get('/stats/gawel_get')
        resp.mustcontain('<tr><td><a href="http://referer0.com" title="http://referer0.com">http://referer0.com</a></td><td>2</td></tr>')
        resp.mustcontain('<tr><td><a href="http://referer1.com" title="http://referer1.com">http://referer1.com</a></td><td>1</td></tr>')

        resp = self.app.get('/json/stats/?alias=gawel_get')
        resp.mustcontain('"url": "http://www.gawel.get"', '"alias": "gawel_get"', '"stats":', '"referer": "http://referer0.com')


