import numpy as np
import os
import timeit
import math
from trank import Mahonian, Mallows
from trank import *

class Partition:
    def __init__(self, N, n):
        self.name = "Partition"
        self.N = N # number of items
        self.n = n # number of samples
        self.m = (self.N * (self.N - 1)) / 2 # max Kendall distance
        self.upperbound = self.n * self.m + 1 # upper bound for the domain
        self.mahonian = Mahonian(N)

        self.set_params()


    def set_params(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fname = dir_path + ('/partition/data_item_%d_sample_size_%d.txt' % (self.N, self.n))
        exists = os.path.isfile(fname)
        if exists:
            with open(fname, 'r') as f:
                for i, line in enumerate(f):
                    self.arr[i] = int(line)
        else:
            #print(self.upperbound)
            self.memo = [[0 for i in range(self.upperbound)] for j in range(self.n+1)]
            for i in range(1,self.n+1): self.memo[i][0] = 1
            for i, v in enumerate(self.mahonian.getArray()): self.memo[1][i] = v
            for i in xrange(1, self.upperbound):
                #print( "  Starting: %d (%d)" % (i,self.upperbound))
                #print( "  %s" % str(self.memo))
                self.rec(self.n, i)
                #print("  %s" % str(self.memo))

            self.arr = [self.memo[self.n][i] for i in range(self.upperbound)]
            self.arr[self.upperbound-1]=1

            with open(fname, 'w') as f:
                for i in self.arr:
                    f.write("%d\n" % i)
                f.close()

    def rec(self, n, l):
        # Base cases
        if (self.memo[n][l] != 0):
            #print(self.memo)
            return self.memo[n][l]

        sum = 0
        for i in range(min(self.m,l)+1):
            if ((l-i>=0) & (n>0) & (l-i <= ((n-1) * self.m) )):
            #if ((l - i >= 0)&(n>0)):
                sum += (self.mahonian.get(i) * self.rec(n - 1, l - i))


        # store result into memo
        self.memo[n][l] = sum
        return sum



    def get(self, l):
        if (l<self.upperbound):
            return self.arr[l]
        else:
            return None

    def getArray(self):
        return self.arr

if __name__ == "__main__":

    phi = 0.2
    samp_num = 5000


    for i in xrange(4,10):
        for n in xrange(2, 40):
            start = timeit.default_timer()

            dir_path = os.path.dirname(os.path.realpath(__file__))
            fname = dir_path + ('/partition/data_item_%d_sample_size_%d.txt' % (i, n))
            exists = os.path.isfile(fname)
            if exists:
                os.remove(fname)

            print( "------------ items: %d, sample size %d ---------" % (i,n) )
            partition = Partition(i, n)

            #print("%g" % partition.get(i-2))
            print(["%g" % j for j in partition.getArray()] )


            stop = timeit.default_timer()

            print("Time: %g" % (stop - start))


            # compare expected value
            pi0 = range(1,i+1)
            mallows = Mallows(pi0, phi)
            # s = 0.0
            # for j in range(samp_num):
            #     for l in range(n):
            #         s += kendall_tau(pi0, mallows.get_sample())
            # print("Expected distance (sampling) : %g" % (s/samp_num))

            s = 0.0
            for ind, v in enumerate(partition.mahonian.getArray()):
                prob = v * (np.power(phi,ind) /mallows.get_normalization() ) # this is the probability that we see a rnaking with distance i
                s += ind * prob
            print("Expected distance (Mahonian) : %g" % (n*s))
            print("Expected distance (log part) : %g" % (n*mallows.expected_sufficient_stat()))

            s = 0.0
            normalization = np.power( mallows.get_normalization(),n)
            for ind, v in enumerate(partition.getArray()):
                s += ind * ((np.power(phi,ind) * v) / normalization)

            print("Expected distance (partition): %g" % (s))