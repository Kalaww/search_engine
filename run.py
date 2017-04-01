#!/usr/bin/python

import sys
import os
import logging as log
from optparse import OptionParser

from search_engine.pagerank import Pagerank
from search_engine.structure.graph import Graph
import search_engine.wiki_collector as wiki_collector
from search_engine.search import search

DEFAULT_DICTIONARY = 'data/dictionary.fr.csv'

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
                        help='FILE words dictionary in csv [default: %default]', default=DEFAULT_DICTIONARY)
collector_op.add_option('-i', '--print-interval', action='store', type='int', dest='interval', metavar='VALUE', default=100000,
                        help='print progress each VALUE lines [default: %default]')
collector_op.add_option('-l', '--line-count', action='store', type='int', dest='lines', metavar='LINES',
                        help='specify the number of lines in the wiki file, it avoids the programm to look for it')
collector_op.add_option('-p', '--pages-per-word', action='store', type='int', dest='pages_per_word', metavar='NUMBER',
                        help='NUMBER of pages per word to save [default: %default]', default=10)

search_op = OptionParser(usage='usage: %prog search [options]')
search_op.add_option('-d', '--dictionary', action='store', type='string', dest='dictionary', metavar='FILE',
                        help='FILE words dictionary in csv [default: %default]', default=DEFAULT_DICTIONARY)
search_op.add_option('-w', '--words-appearance', action='store', type='string', dest='words_appearance', metavar='FILE',
                        help='FILE words appearance in page filename')
search_op.add_option('-p', '--pagescore', action='store', type='string', dest='pagescore', metavar='FILE',
                        help='FILE pagescore filename')
search_op.add_option('-i', '--pageID-to-title', action='store', type='string', dest='pageID_to_title', metavar='FILE',
                        help='FILE pageID_to_title filename')
search_op.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
                       help='verbose mode')


both_op = OptionParser(usage='usage: %prog both [options]')
both_op.add_option('-d', '--dictionary', action='store', type='string', dest='dictionary', metavar='FILE',
                        help='FILE words dictionary in csv [default: %default]', default=DEFAULT_DICTIONARY)
both_op.add_option('-w', '--wiki', action='store', type='string', dest='wiki', metavar='FILE',
                        help='FILE that contains a wiki dump')
both_op.add_option('-o', '--output-dir', action='store', type='string', dest='dir', metavar='FILE',
                        help='FILE output directory where to store collected data')
both_op.add_option('-i', '--print-interval', action='store', type='int', dest='interval', metavar='VALUE', default=100000,
                        help='print progress each VALUE lines [default: %default]')
both_op.add_option('-l', '--line-count', action='store', type='int', dest='lines', metavar='LINES',
                        help='specify the number of lines in the wiki file, it avoids the programm to look for it')
both_op.add_option('-p', '--pages-per-word', action='store', type='int', dest='pages_per_word', metavar='NUMBER',
                        help='NUMBER of pages per word to save [default: %default]', default=10)
both_op.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
                       help='verbose mode')
both_op.add_option('-e', '--epsilon', action='store', dest='epsilon', type='float', default=0.0001,
                       help='page rank epsilon [default: %default]')
both_op.add_option('-z', '--zap', action='store', dest='zap', type='float', default=0.0,
                       help='zap factor [default: %default]')
both_op.add_option('-s', '--step', action='store_true', dest='print_step', default=False,
                       help='print number of step')
both_op.add_option('-a', '--starter', action='store', type='string', dest='starter', default='all',
                       help='starter vertex for the page rank vector: index of the vertex or \'all\' for all vertices [default: %default]')


def usage():
    print('Commands available:')
    print('\tpagerank\texecute pagerank')
    print('\tcollector\texecute collector')
    print('\tsearch\t\texecute search')
    print('\tboth\t\texecute collector then pagerank')


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
    elif args[0] == 'search':
        run_search(args[1:])
    elif args[0] == 'both':
        run_both(args[1:])
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
        print('Error: need to specify a graph file')
        pagerank_op.print_help()
        return

    graph = Graph(options.graph_filename)
    p = Pagerank(graph, options.starter, zap=options.zap, epsilon=options.epsilon, verbose=options.verbose)
    result = p.run(options.print_step)

    if result is None:
        return

    if options.output:
        with open(options.output, 'w') as fd:
            for id, score in enumerate(result):
                fd.write('{} {}\n'.format(id, score))
    else:
        for id, score in enumerate(result):
            print('{} {}'.format(id, score))


def run_collector(args):
    global collector_op

    (options, args_left) = collector_op.parse_args(args=args)

    if not options.wiki:
        print('Error: missing wiki dump filename')
        collector_op.print_help()
        return
    if not options.dir:
        print('Error: missing ouput directory')
        collector_op.print_help()
        return
    if not options.dictionary:
        print('Error: missing words dictionary filename')
        collector_op.print_help()
        return
    if options.lines:
        lines = options.lines
    else:
        lines = None

    wiki_collector.run(
        options.wiki,
        options.dir,
        options.dictionary,
        options.interval,
        options.pages_per_word,
        lines_count=lines,
    )


def run_both(args):
    global both_op

    (options, args_left) = both_op.parse_args(args=args)

    if not options.wiki:
        print('Error: missing wiki dump filename')
        both_op.print_help()
        return
    if not options.dir:
        print('Error: missing ouput directory')
        both_op.print_help()
        return
    if not options.dictionary:
        print('Error: missing words dictionary filename')
        both_op.print_help()
        return
    if options.lines:
        lines = options.lines
    else:
        lines = None

    if options.verbose:
        log.basicConfig(level=log.DEBUG)
    else:
        log.basicConfig(level=log.INFO)

    pageID_to_title_filename, page_links_filename, words_appearance_filename = wiki_collector.run(
        options.wiki,
        options.dir,
        options.dictionary,
        options.interval,
        options.pages_per_word,
        lines_count=lines,
    )

    page_score_filename = os.path.join(options.dir, 'page_score.txt')


    print('\nRUN PAGE RANK')
    graph = Graph(page_links_filename)
    p = Pagerank(graph, options.starter, zap=options.zap, epsilon=options.epsilon, verbose=options.verbose)
    result = p.run(options.print_step)

    if result is None:
        return

    with open(page_score_filename, 'w') as fd:
        for id, score in enumerate(result):
            fd.write('{} {}\n'.format(id, score))

    print('\n--------------------------------------')
    print('Now, you can search with this command :')
    print('python3 run.py search -w {} -p {} -i {} -d {}'.format(
        words_appearance_filename,
        page_score_filename,
        pageID_to_title_filename,
        options.dictionary
    ))


def run_search(args):
    global search_op

    (options, args_left) = search_op.parse_args(args=args)

    if not options.dictionary:
        print('Error: missing words dictionary filename')
        search_op.print_help()
        return
    if not options.words_appearance:
        print('Error: missing words appearance filename')
        search_op.print_help()
        return
    if not options.pagescore:
        print('Error: missing pagescore filename')
        search_op.print_help()
        return
    if not options.pageID_to_title:
        print('Error: missing pageID_to_title filename')
        search_op.print_help()
        return

    search(
        options.dictionary,
        options.words_appearance,
        options.pagescore,
        options.pageID_to_title,
        verbose=options.verbose
    )

if __name__ == '__main__':
    main()