# -*- coding: utf-8 -*-
from optparse import OptionParser
from aupoil.cli import url

usage = "%prog [options] url"

parser = OptionParser()
parser.usage = usage
parser.add_option("-a", "--alias", dest="alias",
                  action="store", default=None,
                  help="url's alias")
parser.add_option("-s", "--stats", dest="stats",
                  action="store_true", default=False,
                  help="print stats for url or alias")
parser.add_option("--server", dest="server",
                  action="store", default='http://a.pwal.fr',
                  help="server. default to a.pwal.fr")

def main():
    (options, args) = parser.parse_args()
    if not args and not options.stats:
        parser.parse_args(['-h'])

    value = args and args[0] or ''
    if options.stats:
        result = url.stats(value, options.alias, options.server)
        if 'stats' in result:
            print 'Stats for %(alias)s - %(url)s' % result
            for i in result.get('stats', []):
                print '%(referer)30s\t%(count)5s' % i
        elif result.get('error'):
            print result['error']
    elif value:
        result = url.add(value, options.alias, options.server)
        if 'new_url' in result:
            print result['new_url']
        elif result.get('error'):
            print result['error']
        else:
            print result
