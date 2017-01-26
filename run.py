#!/usr/bin/python

import sys
import logging as log
from optparse import OptionParser

from search_engine.pagerank import Pagerank
from search_engine.structure.graph import Graph

pagerank_op = OptionParser(usage='usage: %prog pagerank [options]')
pagerank_op.add_option('-g', '--graph', action='store', type='string', dest='graph_filename',
                       help='FILE that contains a graph', metavar='FILE')
pagerank_op.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
                       help='verbose mode')
pagerank_op.add_option('-e', '--epsilon', action='store', dest='epsilon', type='float', default=0.0001,
                       help='page rank epsilon [default: %default]')
pagerank_op.add_option('-z', '--zap', action='store', dest='zap', type='float', default=0.0,
                       help='zap factor [default: 0.0]')
pagerank_op.add_option('-o', '--output', action='store', dest='output',
                       help='FILE to store the page rank vector [default: stdout]', metavar='FILE')
pagerank_op.add_option('-s', '--step', action='store_true', dest='print_step', default=False,
                       help='print number of step')
pagerank_op.add_option('-a', '--starter', action='store', type='int', dest='starter', default=0,
                       help='starter vertex for the page rank vector [default: %default]')


def usage():
    global pagerank_op

    print '== PAGE RANK =='
    pagerank_op.print_help()


def main():
    global pagerank_op
    args = sys.argv[1:]

    if len(args) == 0:
        usage()
        return

    if args[0] == 'pagerank':
        run_pagerank(args[1:])
    else:
        usage()


def run_pagerank(args):
    global pagerank_op

    (options, args_left) = pagerank_op.parse_args()

    if options.verbose:
        log.basicConfig(level=log.DEBUG)
    else:
        log.basicConfig(level=log.INFO)

    if not options.graph_filename:
        pagerank_op.error('need to specify a graph file')
        return

    graph = Graph(options.graph_filename)
    p = Pagerank(graph, options.starter, zap=options.zap, epsilon=options.epsilon, verbose=options.verbose)
    result = p.run(options.print_step)

    if not result:
        return

    if options.output:
        with open(options.output, 'w') as fd:
            for i in result:
                fd.write('{}\n'.format(i))
    else:
        for i in result:
            print('{}'.format(i))


if __name__ == '__main__':
    main()