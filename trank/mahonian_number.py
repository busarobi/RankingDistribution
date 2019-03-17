import numpy as np
import os
import timeit
from math import factorial
from trank import *

class Mahonian:
    def __init__(self, N):
        self.name = "Mahonian"
        self.N = N
        self.set_params()

    def set_params(self):
        self.m = (self.N * (self.N - 1)) / 2 + 1
        self.halfm = int(np.ceil(self.m/2.0))
        self.arr = [0 for i in range(self.m)]

        dir_path = os.path.dirname(os.path.realpath(__file__))
        fname = dir_path + ('/inversions/data_%d.txt' % self.N)
        exists = os.path.isfile(fname)
        if exists:
            with open(fname, 'r') as f:
                for i, line in enumerate(f):
                    self.arr[i] = int(line)
        else:
            self.arr[0] = 1
            self.memo = [[0 for i in range(self.m)] for j in range(self.N+1)]
            #for i in xrange(self.N+1): self.memo[i][0]=1
            for i in xrange(1, self.halfm):
                #print(i)
                #print(self.memo)

                self.rec(self.N, i)
                self.arr[i] = self.memo[self.N][i]

            for i in xrange(self.halfm):
                self.arr[self.m-i-1] = self.arr[i]

            with open(fname, 'w') as f:
                for i in self.arr:
                    f.write("%d\n" % i)
                f.close()


    def rec(self, N, K):

        # Base cases
        if (N == 0): return 0
        if (K == 0):
            self.memo[N][K]=1
            return 1

        # If already solved then
        # return result directly
        if (self.memo[N][K] != 0):
            return self.memo[N][K]

        # Calling recursively all subproblem
        # of permutation size N - 1
        sum = 0
        for i in range(K + 1):

            # Call recursively only if
            # total inversion to be made
            # are less than size
            if (i <= N - 1):
                if (self.memo[N-1][K-i] != 0):
                    sum += self.memo[N - 1][K - i]
                else:
                    sum += self.rec(N - 1, K - i)

        # store result into memo
        self.memo[N][K] = sum
        self.memo[N][((N*(N-1))/2) - i]=self.memo[N][K]
        return sum

    def get(self, k):
        if (k<self.m):
            return self.arr[k]
        else:
            return None

    def getArray(self):
        return self.arr

if __name__ == "__main__":
    samp_num = 10000

    for i in xrange(4,20):
        start = timeit.default_timer()

        dir_path = os.path.dirname(os.path.realpath(__file__))
        fname = dir_path + ('/inversions/data_%d.txt' % i)
        exists = os.path.isfile(fname)
        if exists:
            os.remove(fname)

        print( "------------ %d ---------" % i )
        mahonian = Mahonian(i)


        stop = timeit.default_timer()

        print("Time: %g" % (stop - start))

        #
        print("%g" % mahonian.get(i-2))
        print(["%g" % j for j in mahonian.getArray()] )
        print( "%d %d" % (np.sum(mahonian.getArray()), factorial(i)))
        assert(np.sum(mahonian.getArray() != factorial(i)))


        phi = 0.2
        pi0=range(1,i+1)
        mallows = Mallows(pi0, phi)
        s = 0.0
        for i, v in enumerate(mahonian.getArray()):
            prob = v * (np.power(phi,i) /mallows.get_normalization() ) # this is the probability that we see a rnaking with distance i
            s += i * prob
        print("Expected distance (Mahonian): %g" % (s))
        print("Expected distance (log part): %g" % (mallows.expected_sufficient_stat()))

        s = 0.0
        for j in range(samp_num):
            s += kendall_tau(pi0, mallows.get_sample())
        print("Expected distance (sampling) : %g" % (s/samp_num))
