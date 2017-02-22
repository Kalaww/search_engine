#!/usr/bin/python

import sys
import logging as log
from optparse import OptionParser

from search_engine.pagerank import Pagerank
from search_engine.structure.graph import Graph
import search_engine.wiki_dump_collector as wiki_dump_collector

pagerank_op = OptionParser(usage='usage: %prog pagerank [options]')
pagerank_op.add_option('-g', '--graph', action='store', type='string', dest='graph_filename',
                       help='FILE that contains a graph', metavar='FILE')
pagerank_op.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
                       help='verbose mode')
pagerank_op.add_option('-e', '--epsilon', action='store', dest='epsilon', type='float', default=0.0001,
                       help='page rank epsilon [default: %default]')
pagerank_op.add_option('-z', '--zap', action='store', dest='zap', type='float', default=0.0,
                       help='zap factor [default: %default]')
pagerank_op.add_option('-o', '--output', action='store', dest='output',
                       help='FILE to store the page rank vector [default: stdout]', metavar='FILE')
pagerank_op.add_option('-s', '--step', action='store_true', dest='print_step', default=False,
                       help='print number of step')
pagerank_op.add_option('-a', '--starter', action='store', type='string', dest='starter', default='all',
                       help='starter vertex for the page rank vector: index of the vertex or \'all\' for all vertices [default: %default]')


collector_op = OptionParser(usage='usage: %prog collector [options]')
collector_op.add_option('-w', '--wiki', action='store', type='string', dest='wiki', metavar='FILE',
                        help='FILE that contains a wiki dump')
collector_op.add_option('-o', '--output-dir', action='store', type='string', dest='dir', metavar='FILE',
                        help='FILE output directory where to store collected data')
collector_op.add_option('-d', '--dictionary', action='store', type='string', dest='dictionary', metavar='FILE',
                        help='FILE words dictionary in csv')
collector_op.add_option('-i', '--print-interval', action='store', type='int', dest='interval', metavar='VALUE', default=100000,
                        help='print progress each VALUE lines [default: %default]')


def usage():
    global pagerank_op, collector_op

    print('== PAGE RANK ==')
    pagerank_op.print_help()

    print('\n== COLLECTOR ==')
    collector_op.print_help()

def main():
    global pagerank_op
    args = sys.argv[1:]

    if len(args) == 0:
        usage()
        return

    if args[0] == 'pagerank':
        run_pagerank(args[1:])
    elif args[0] == 'collector':
        run_collector(args[1:])
    else:
        usage()


def run_pagerank(args):
    global pagerank_op

    (options, args_left) = pagerank_op.parse_args(args=args)

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

    if result is None:
        return

    if options.output:
        with open(options.output, 'w') as fd:
            for i in result:
                fd.write('{}\n'.format(i))
    else:
        for i in result:
            print('{}'.format(i))


def run_collector(args):
    global collector_op

    (options, args_left) = collector_op.parse_args(args=args)

    if not options.wiki:
        collector_op.error('missing wiki dump filename')
        return
    if not options.dir:
        collector_op.error('missing ouput directory')
        return
    if not options.dictionary:
        collector_op.error('missing words dictionary filename')
        return

    wiki_dump_collector.run(
        options.wiki,
        options.dir,
        options.dictionary,
        options.interval
    )


if __name__ == '__main__':
    main()