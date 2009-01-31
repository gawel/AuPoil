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

test_db = os.path.join(conf_dir, 'AuPoil', 'dev.db')
if os.path.isfile(test_db):
    os.remove(test_db)

config = {'__file__':os.path.join(conf_dir, 'AuPoil', 'test.ini')}

SetupCommand('setup-app').run([config['__file__']])

class TestBase(TestCase):

    def __init__(self, *args, **kwargs):
        wsgiapp = loadapp('config:%s' % config['__file__'])
        self.app = TestApp(wsgiapp)
        TestCase.__init__(self, *args, **kwargs)

    def test_alias(self):
        resp = self.app.get('/')
        form = resp.forms['aupoil_form']
        form['url'] = 'http://www.gawel.org'
        form['alias'] = 'gawel'
        resp = form.submit()
        resp.mustcontain('http://localhost/gawel')

        resp = self.app.get('/gawel')
        assert resp.headers.get('location') == 'http://www.gawel.org', resp

    def test_noalias(self):
        resp = self.app.get('/')
        form = resp.forms['aupoil_form']
        form['url'] = 'http://www.gawel.nu'
        resp = form.submit()
        resp.mustcontain('http://localhost/')

        form = resp.forms['aupoil_result_form']
        alias = form['result'].value.split('/')[-1]
        assert alias is not None, form['result'].value
        resp = self.app.get('/%s' % alias)
        assert resp.headers.get('Location') == 'http://www.gawel.nu', resp

    def test_put_alias(self):
        resp = self.app.put('/gawel_put', params='http://www.gawel.put')
        resp.mustcontain("{'url': 'http://www.gawel.put', 'new_url': 'http://localhost/gawel_put', 'code': 0}")

        resp = self.app.put('/gawel_put', params='http://www.gawel.org')
        resp.mustcontain("{'code': 1, 'error': 'http://www.gawel.org is already bind to http://localhost/gawel'}")

        resp = self.app.put('/gawel_put', params='http://www.gawel.put2')
        resp.mustcontain("{'code': 1, 'error': u'http://localhost/gawel_put is already bind to http://www.gawel.put'}")

    def test_put(self):
        resp = self.app.put('/', params='http://www.noalias.put')
        resp.mustcontain("{'url': 'http://www.noalias.put', 'new_url': 'http://localhost/","', 'code': 0}")

    def test_invalid_url(self):
        resp = self.app.put('/', params='www.gawel.org')
        resp.mustcontain("You must provide a valid url")

        resp = self.app.put('/', params='ssh://www.gawel.org')
        resp.mustcontain("You must provide a valid url")

        resp = self.app.put('/', params='http:/www.gawel.org')
        resp.mustcontain("You must provide a valid url")

