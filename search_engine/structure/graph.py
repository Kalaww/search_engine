import re
import logging as log

from matrix import Matrix
from search_engine.exception import GrapheException

class Graph:

    ORIENTED = True
    NON_ORIENTED = False

    def __init__(self, filename, orientation=ORIENTED):
        self.nb_vertices = 0
        self.nb_arcs = 0
        self.is_directed = orientation
        self.filename = filename
        self.matrix = None
        self.is_loaded = False

        self.read_from_file()

    def read_from_file(self):
        fd = open(self.filename)
        max = 0
        for line in fd.readlines():
            if line.startswith('#') or len(line) == 0:
                continue
            src, dst = self.read_line(line)
            if src > max :
                max = src
            if dst > max :
                max = dst
            self.nb_arcs += 1
        self.nb_vertices = max + 1
        log.debug('Graph first read: {} vertices and {} arcs detected'.format(self.nb_vertices, self.nb_arcs))

        fd.seek(0, 0)
        current_src = 0
        current_succs = []
        self.matrix = Matrix(self.nb_arcs, self.nb_vertices)

        for line in fd.readlines():
            if line.startswith('#') or len(line) == 0:
                continue
            src, dst = self.read_line(line)
            if src == current_src:
                current_succs.append(dst)
            else:
                self.matrix.put_row(current_src, current_succs)
                current_src = src
                current_succs = [dst]
        self.matrix.put_row(current_src, current_succs)
        self.matrix.end()
        self.is_loaded = True
        log.info('Graph loaded with success')

    def read_line(self, line):
        match = re.match('(\d+)\s+(\d+)', line)
        if match is None:
            raise GrapheException('Cannot read line "{}" in file {}'.format(line, self.filename))
        src = int(match.group(1))
        dst = int(match.group(2))
        return (src, dst)