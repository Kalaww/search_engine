import logging as log
from optparse import OptionParser

from graph import Graph
from pagerank import Pagerank


def main():
    op = OptionParser(usage='usage: %prog [options]')
    op.add_option('-g', '--graph', action='store', type='string', dest='graph_filename',
                       help='file FILE containing the graph', metavar='FILE')
    op.add_option('-v', '--verbose', action='store_true', dest='verbose', default=True,
                       help='verbose mode')

    (options, args) = op.parse_args()

    if options.verbose:
        log.basicConfig(level=log.DEBUG)
    else:
        log.basicConfig(level=log.INFO)

    if not options.graph_filename:
        op.error('need to specify a graph file')
        return

    g = Graph(options.graph_filename)
    p = Pagerank(g, 0)
    p.run()
    print(p.vector)

if __name__ == '__main__':
    main()