# -*- coding: utf-8 -*-
import subprocess
import os, sys

version = sys.argv[1]

os.chdir('apwalfr')

fd = open('install.rdf')
lines = fd.readlines()
fd.close()
fd = open('install.rdf', 'w')
for l in lines:
    print l
    if 'em:version' in l:
        l = '                   em:version="%s"\n' % version
    fd.write(l)
fd.close()
subprocess.call('zip -r ../apwal-%s.xpi *' % version, shell=True)
subprocess.call('hg ci -m "plugin version %s"' % version, shell=True)
