# -*- coding: utf-8 -*-
#
import scipy.sparse
import scipy.sparse.linalg
import numpy

import pycont


class Bratu1d(object):
    def __init__(self):
        self.n = 6
        h = 1.0 / (self.n - 1)
        self.A = (
            1.0
            / h ** 2
            * scipy.sparse.diags([1.0, -2.0, 1.0], [-1, 0, 1], shape=(self.n, self.n))
        )
        return

    def f(self, u, lmbda):
        out = self.A.dot(u) + lmbda * numpy.exp(u)
        out[0] = u[0]
        out[-1] = u[-1]
        return out

    def df_dlmbda(self, u, lmbda):
        out = numpy.exp(u)
        out[0] = 0.0
        out[-1] = 0.0
        return out

    def jacobian_solver(self, u, lmbda, rhs):
        M = self.A.copy()
        d = M.diagonal()
        d += lmbda * numpy.exp(u)
        M.setdiag(d)
        # Dirichlet conditions
        assert numpy.all(M.offsets == [-1, 0, 1])
        M.data[0][self.n - 2] = 0.0
        M.data[1][0] = 1.0
        M.data[1][self.n - 1] = 1.0
        M.data[2][1] = 0.0
        return scipy.sparse.linalg.spsolve(M, rhs)


def test_pycont():
    problem = Bratu1d()
    u0 = numpy.zeros(problem.n)
    lmbda0 = 0.0

    def callback(k, lmbda, sol):
        print("Step {}: Found solution for lmbda = {}".format(k, lmbda))
        return

    pycont.natural(problem, u0, lmbda0, callback, max_steps=5)
    return


if __name__ == "__main__":
    test_pycont()
