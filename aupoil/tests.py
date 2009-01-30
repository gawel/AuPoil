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

test_db = os.path.join(conf_dir, 'test.db')
if os.path.isfile(test_db):
    os.remove(test_db)

config = {'__file__':os.path.join(conf_dir, 'AuPoil', 'test.ini')}

SetupCommand('setup-app').run([config['__file__']])

class TestBase(TestCase):

    def __init__(self, *args, **kwargs):
        wsgiapp = loadapp('config:%s' % config['__file__'])
        self.app = TestApp(wsgiapp)
        url._push_object(URLGenerator(config['routes.map'], environ))
        TestCase.__init__(self, *args, **kwargs)


