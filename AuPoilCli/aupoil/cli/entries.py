# -*- coding: utf-8 -*-
from optparse import OptionParser
from aupoil.cli import url

usage = "%prog [options] url"

parser = OptionParser()
parser.usage = usage
parser.add_option("-a", "--alias", dest="alias",
                  action="store", default=None,
                  help="url's alias")
parser.add_option("-s", "--server", dest="server",
                  action="store", default='http://a.pwal.fr',
                  help="server. default to a.pwal.fr")

def main():
    (options, args) = parser.parse_args()
    if not args:
        parser.parse_args(['-h'])
    value = args[0]
    result = url.add(value, options.alias, options.server)
    if 'new_url' in result:
        print result['new_url']
    elif result.get('error'):
        print result['error']
    else:
        print result
