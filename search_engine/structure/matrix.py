import numpy as np

from search_engine.exception import MatrixException

class Matrix:

    def __init__(self, nb_value, size):
        self.nb_value = nb_value
        self.size = size

        self.values = np.zeros(self.nb_value, dtype=np.float64)
        self.lines = np.zeros(self.size + 1, dtype=np.uint8)
        self.indexes = np.zeros(self.nb_value, dtype=np.uint8)

        self.lines[self.size] = self.nb_value

        self.values_it = 0
        self.indexes_it = 0

        self.last_row_index = 0
        self.last_column_index = 0

    def __len__(self):
        return self.size

    def put(self, row, column, value):
        if row < self.last_row_index:
            raise MatrixException('Try to add row {} after row {}'.format(row, self.last_row_index))
        if row == self.last_row_index and column <= self.last_column_index:
            raise MatrixException('Try to add column {} after column {} in the same row {}'.format(
                column, self.last_column_index, row
            ))

        if row != self.last_row_index:
            for i in range(self.last_row_index +1, row +1):
                self.lines[i] = self.values_it

        self.values[self.values_it] = value
        self.values_it += 1

        self.indexes[self.indexes_it] = column
        self.indexes_it += 1

        self.last_row_index = row
        self.last_column_index = column

    def put_row(self, row, columns):
        if row < self.last_row_index:
            raise MatrixException('Try to add row {} after row {}'.format(row, self.last_row_index))

        value = 1. / float(len(columns))

        self.lines[row] = self.values_it
        if row != self.last_row_index:
            for i in range(self.last_row_index +1, row +1):
                self.lines[i] = self.values_it

        for column in columns:
            self.values[self.values_it] = value
            self.indexes[self.indexes_it] = column
            self.indexes_it += 1
            self.values_it += 1

        self.last_row_index = row
        self.last_column_index = 0

    def end(self):
        for i in range(self.last_row_index +1, len(self.lines) -1):
            self.lines[i] = self.values_it

    def __str__(self):
        s = 'C:\n'
        for i in self.values:
            s += str(i) + ' '
        s += '\nL:\n'
        for i in self.lines:
            s += str(i) + ' '
        s += '\nI:\n'
        for i in self.indexes:
            s += str(i) + ' '
        return s + '\n'

    def multiply_transpose_with(self, vector):
        if len(vector) != self.size:
            raise MatrixException('Vector size is not the same as matrix')

        res = np.zeros(self.size, dtype=np.float64)

        for row in range(0, self.size):
            for i in range(self.lines[row], self.lines[row+1]):
                res[self.indexes[i]] = res[self.indexes[i]] + self.values[i] * vector[row]
        return res