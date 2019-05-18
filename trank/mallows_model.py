from model import *
import numpy as np
from ranking_utils import *
import itertools
from lehmer import int_from_perm, perm_from_int
import math
import matplotlib.pyplot as plt

class Mallows(Model):
    def __init__(self, ranking, phi):
        self.name = "Mallows"
        self.set_params(ranking, phi)
        np.random.seed()

    def set_params(self, ranking, phi):
        # center ranking and ordering
        self.central_ranking = ranking
        self.ordering = order2ranking(ranking)

        # spread
        self.phi = phi
        if (phi>0):
            self.theta = np.log(phi)
        else:
            self.theta = np.inf
        self.order = len(self.central_ranking)

        # Repeated Insertion Sort based sampling
        self.RIMP = np.zeros((self.order, self.order))

        for i1 in range(self.order):
            for i2 in range(i1, self.order):
                self.RIMP[i1][i2] = np.power(self.phi, (i2 - i1)) * ((1 - self.phi) / (1 - np.power(self.phi, (i2+1))))

        # normalization
        self.set_normalization()

    def compute_normalization(self):
        ret_val = 1.0
        for i1 in range(1, self.order):
            tmp_sum = 0.0
            for i2 in range(0, i1 + 1):
                tmp_sum += np.power(self.phi, i2)

            ret_val *= tmp_sum
        return ret_val

    def set_normalization(self):
        self.normalization = 1.0
        for i1 in range(1, self.order):
            tmp_sum = 0.0
            for i2 in range(0, i1 + 1):
                tmp_sum += np.power(self.phi, i2)

            self.normalization *= tmp_sum

    def expected_sufficient_stat(self):
        ret_val = 0.0
        for i1 in range(1, self.order):
            tmp_sum_enum = 0.0
            tmp_sum_denum = 0.0
            for i2 in range(0, i1 + 1):
                tmp_sum_enum += (i2 * np.exp(self.theta * i2))
                tmp_sum_denum += np.exp(self.theta * i2)

            ret_val += (tmp_sum_enum / tmp_sum_denum)
        return ret_val

    # def expected_sufficient_stat(self):
    #     ret_val = 0.0
    #     for i1 in range(1, self.order):
    #         tmp_sum_enum = 0.0
    #         for i2 in range(1, i1 + 1):
    #             tmp_sum_enum += (i2 * np.exp(self.theta * (i2-1)))
    #
    #
    #         ret_val += tmp_sum_enum
    #     return ret_val


    # based on Fligner, there is some bug in this code
    # def expected_sufficient_stat(self):
    #     ret_val = 0.0
    #     tmp_sum_enum = self.order * np.exp(self.theta)
    #     tmp_sum_denum = 1.0 - np.exp(self.theta)
    #     ret_val = (tmp_sum_enum / tmp_sum_denum)
    #
    #     for i2 in range(1, self.order + 1):
    #         tmp_sum_enum = (i2 * np.exp(self.theta * i2))
    #         tmp_sum_denum = (1.0-np.exp(self.theta * i2))
    #
    #         ret_val -= (tmp_sum_enum / tmp_sum_denum)
    #     return ret_val

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
            sample[r] = self.ordering[i1]
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

    # def get_multinomial_distribution(self):
    #     dist = np.zeros((self.order * (self.order-1)/2+1,))
    #     for i1 in range(self.order*(self.order-1)/2+1):
    #         nd = numberOfPermWithKInversion(self.order, i1)
    #         # print("Number of inversion: %d, number of permuation: %d" % (i1, nd))
    #         dist[i1] = (nd * np.power(self.phi, i1)) / self.normalization
    #     return dist

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

    def get_normalization(self):
        return self.normalization


if __name__ == "__main__":
    M = 5
    phi1 = 0.1
    phi2 = 0.1

    model = Mallows( range(1,M+1), phi1 )
    dist = model.get_multinomial_distribution()
    print(dist)
    model2 = Mallows( range(M, 0, -1), phi2 )
    dist2 = model2.get_multinomial_distribution()
    print(dist2)
    print( "Difference:")
    print(dist - dist2)

    chis = np.zeros((model.order*(model.order-1)/2+1,))
    chis[0] = np.power(dist[0] - dist2[0],2) / dist2[0]
    for i1 in range(1,model.order*(model.order-1)/2+1):
        chis[i1] = chis[i1-1] + np.power(dist[i1] - dist2[i1],2) / dist2[i1]

    idx = range(model.order*(model.order-1)/2+1)
    plt.plot(idx, dist, label="Mallows model $\phi = %g$" % phi1)
    plt.plot(idx, dist2, label="Mallows model $\phi = %g$" % phi2)
    plt.plot(idx, np.abs(dist - dist2), label="Difference")
    plt.plot(idx, chis, label="$\chi^2_q$")
    plt.grid(True)
    plt.legend()
    plt.show()

    # assert( np.sum(dist) != 1.0 )
    # sample = model.get_sample()
    # print(sample)
    #
    # model.test_sampling()