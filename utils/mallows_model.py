from model import *
import numpy as np
from ranking_utils import *
import itertools
from lehmer import int_from_perm, perm_from_int
import math

class Mallows(Model):
    def __init__(self, ranking, phi):
        self.name = "Mallows"
        self.set_params(ranking, phi)

    def set_params(self, ranking, phi):
        # center ranking and ordering
        self.central_ranking = ranking
        self.ordering = order2ranking(ranking)

        # spread
        self.phi = phi
        self.theta = -np.log(phi)
        self.order = len(self.central_ranking)

        # Repeated Insertion Sort based sampling
        self.RIMP = np.zeros((self.order, self.order))

        for i1 in range(self.order):
            for i2 in range(i1, self.order):
                self.RIMP[i1,i2] = np.power(self.phi, (i2 - i1)) * ((1 - self.phi) / (1 - np.power(self.phi, (i2+1))))

        # normalization
        self.normalization = normalizationMallows(self.order, self.phi)

    def get_sample(self):
        sample = np.zeros((self.order,), dtype=np.int32)
        sample[0] = self.ordering[0]
        for i1 in range(1,self.order):
            p = self.RIMP[0:(i1+1), i1]

            # index to insert
            r = np.nonzero(np.random.multinomial(1, p))[0][0]

            # shift to the right
            for o in range(i1,r,-1):
                sample[o] = sample[o-1]

            # insert
            sample[r] = model.ordering[i1]
        return sample

    def get_probability(self, perm):
        prob = np.power(self.phi, kendall_tau(self.central_ranking, perm))
        return prob / self.normalization

    def get_distribution(self):
        dist = np.zeros((math.factorial(self.order),))
        L = np.arange(1, self.order + 1)
        for i1 in range(math.factorial(self.order)):
            perm = perm_from_int(L,i1)
            dist[i1] = self.get_probability(perm)
        return dist

    def get_multinomial_distribution(self):
        dist = np.zeros((self.order * (self.order-1)/2,))
        
        return dist

    def test_sampling(self):
        freq = np.zeros((math.factorial(self.order),))
        L = np.arange(1, self.order+1)
        n = 100000

        for i1 in range(n):
            sample = self.get_sample()
            idx = int_from_perm(L, sample)
            freq[idx] += 1

        p_hat = freq / float(n)

        for i1 in range(math.factorial(self.order)):
            perm = perm_from_int(L,i1)
            p = self.get_probability(perm)
            print(perm, p_hat[i1], p)


if __name__ == "__main__":
    M = 4
    model = Mallows( range(1,M+1), 0.1 )
    sample = model.get_sample()
    print(sample)

    model.test_sampling()