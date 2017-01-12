import sys
import logging as log

from graph import Graph

DIR_DATA = '../data/'


def main(args):
    log.basicConfig(level=log.DEBUG)
    g = Graph(DIR_DATA + 'p2p-Gnutella08.txt')


if __name__ == '__main__':
    main(sys.argv[:1])