import sys
from matrix import Matrix


def main(args):
    m = Matrix(6, 4)
    m.put_row(0, [1, 2, 3])
    m.put_row(1, [0, 2])
    m.put_row(3, [1])
    m.end()
    print(m)

    res = m.multiply_transpose_with([1., 2., 3., 4.])
    print(res)

    n = Matrix(7, 4)
    n.put_row(0, [2])
    n.put_row(1, [0, 1, 3])
    n.put_row(2, [1, 2, 3])
    n.end()
    print(n)

    print(n.multiply_transpose_with([4., 2., 3., 1.]))

if __name__ == '__main__':
    main(sys.argv[:1])