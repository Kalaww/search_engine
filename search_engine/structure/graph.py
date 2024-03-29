import re
import logging as log

from search_engine.structure.matrix import Matrix
from search_engine.exception import GrapheException
from search_engine.util import pretty_number

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
        if self.filename.endswith('.csv'):
            self.read_csv()
        else:
            self.read_txt()

    # def read_csv(self):
    #     fd = open(self.filename)
    #     max = 0
    #     for line in fd.readlines()[1:]:
    #         line_split = line[:-1].split(',', 1)
    #         if len(line_split) != 2:
    #             raise GrapheException('Bad formatting in line {} in file {}'.format(line, self.filename))
    #         src = int(line_split[0])
    #         if src > max :
    #             max = src
    #         if len(line_split[1]) != 0:
    #             dst = [int(d) for d in line_split[1].split(' ') if len(d) > 0]
    #             for d in dst:
    #                 if d > max:
    #                     max = d
    #             self.nb_arcs += len(dst)
    #     self.nb_vertices = max + 1
    #     log.debug('Graph first read: {} vertices and {} arcs detected'.format(self.nb_vertices, self.nb_arcs))
    #
    #     fd.seek(0, 0)
    #     self.matrix = Matrix(self.nb_arcs, self.nb_vertices)
    #
    #     for line in fd.readlines()[1:]:
    #         line_split = line[:-1].split(',', 1)
    #         if len(line_split) != 2:
    #             raise GrapheException('Bad formatting in line {} in file {}'.format(line, self.filename))
    #         if len(line_split[1]) != 0:
    #             src = int(line_split[0])
    #             dst = [int(d) for d in line_split[1].split(' ') if len(d) > 0]
    #             self.matrix.put_row(src, dst)
    #     self.matrix.end()
    #     self.is_loaded = True
    #     log.info('Graph successfully loaded')

    def read_txt(self):
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
        log.info('Graph first read: {} vertices and {} arcs detected'.format(
            pretty_number(self.nb_vertices),
            pretty_number(self.nb_arcs)))

        fd.seek(0, 0)
        current_src = None
        current_succs = []
        self.matrix = Matrix(self.nb_arcs, self.nb_vertices)

        for line in fd.readlines():
            if line.startswith('#') or len(line) == 0:
                continue
            src, dst = self.read_line(line)
            if current_src is not None and src != current_src:
                self.matrix.put_row(current_src, current_succs)
                current_succs = []
            current_src = src
            current_succs.append(dst)
        self.matrix.put_row(current_src, current_succs)
        self.matrix.end()
        self.is_loaded = True
        log.info('Graph successfully loaded')

    def read_line(self, line):
        match = re.match('(\d+)\s+(\d+)', line)
        if match is None:
            raise GrapheException('Cannot read line "{}" in file {}'.format(line, self.filename))
        src = int(match.group(1))
        dst = int(match.group(2))
        return (src, dst)