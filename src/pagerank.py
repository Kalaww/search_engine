import numpy as np
import logging as log


class Pagerank:

    def __init__(self, graph, start, n_steps=None, zap=0.0, epsilon=0.0001, verbose=False):
        self.is_init = False
        if graph is None:
            log.error('Page Rank: graph is None')
            return
        if not graph.is_loaded:
            log.error('Page Rank: graph was not correctly loaded')
            return
        if start < 0 or start >= graph.nb_vertices:
            log.error('Page Rank: start vertex {} out of bound (graph has {} vertices)'.format(start, graph.nb_vertices))
            return

        self.verbose = verbose
        self.graph = graph
        self.start = start
        self.n_steps = n_steps
        self.zap = zap
        self.epsilon = epsilon
        self.vector = np.zeros(graph.nb_vertices, np.float32)
        self.vector[self.start] = 1
        self.is_init = True

    def run(self):
        if not self.is_init:
            log.error('Page Rank: not initialize correctly')
            return
        step = 0
        if self.verbose:
            print('step {}: {}'.format(step, self.vector))
        while True:
            r = self.graph.matrix.multiply_transpose_with(self.vector)
            for i in range(len(r)):
                r[i] = self.zap / len(r) + (1.0 - self.zap) * r[i]
            step += 1
            if self.verbose:
                print('step {}: {}'.format(step, r))

            distance = np.sum(np.abs(r - self.vector))
            self.vector = r.copy()

            if distance < self.epsilon or not self.n_steps is None and step >= self.n_steps:
                break
        log.info('Page Rank: run in {} steps'.format(step))
