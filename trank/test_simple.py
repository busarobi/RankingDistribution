from test import Test
from partition_number import Partition
from mallows_model import Mallows
import numpy as np
from trank import ranking_utils


class SimpleFiniteSample(Test):
    def __init__(self, pi_0, phi, alpha, sample_size):
        self.order = len(pi_0)
        self.alpha = alpha
        self.sampe_size = sample_size
        print( "Generating partition numbers...")
        self.partition = Partition(self.order, self.sampe_size)
        print("Done.")
        self.mallows = Mallows(pi_0, phi)

        self.maxvalueofstat = len(self.partition.getArray())
        self.test_array = np.ones((self.maxvalueofstat,))


        self.normalization = np.power(self.mallows.get_normalization(), self.sampe_size)
        # s = 0.0
        # for i in range(self.maxvalueofstat):
        #     s += self.get_probability_of_stat(i)
        #     print(s,i)
        # print(s)

        expected_value_of_stat = self.sampe_size * self.mallows.expected_sufficient_stat()
        left = int(np.floor(expected_value_of_stat))
        right = int(np.ceil(expected_value_of_stat))
        left_prob = 0.0
        right_prob = 0.0
        power = 0.0

        for i in range(np.round(self.maxvalueofstat/2)):
            lp = self.get_probability_of_stat(left-i)
            if (left_prob+lp < 0.5-self.alpha/2.0):
                left_prob += lp
                self.test_array[left-i] = 0
                power += lp
            else:
                rem =  ((0.5-self.alpha/2.0) - left_prob) # excess in probability
                frac = rem / lp
                power += frac * lp
                self.test_array[left-i] = frac * lp
                break

        for i in range(np.round(self.maxvalueofstat/2)):
            rp = self.get_probability_of_stat(right+i)
            if (right_prob+rp < 0.5-self.alpha/2.0):
                right_prob += rp
                self.test_array[right+i] = 0
                power += rp
            else:
                rem =  ((0.5-self.alpha/2.0) - right_prob) # excess in probability
                frac = rem / rp
                power += frac * rp
                self.test_array[right+i] = frac * rp
                break

        assert(np.abs((1.0-power)-alpha)>10e-4)

    def get_probability_of_stat(self, l):
        frac = np.power(self.mallows.phi, l) / self.normalization
        frac *= self.partition.get(l)
        return frac

    def to_string(self):
        s = ""
        for i, v in enumerate(self.test_array):
            if (v<1.0):
                s += "%d %.8f " % (i,v)
        return s

    def test(self, data):
        assert(len(data) == self.sampe_size)
        s = np.zeros((self.sampe_size,))
        for i, r in enumerate(data):
            s[i] = ranking_utils.kendall_tau(self.mallows.central_ranking, r)

        statistic = np.sum(s)
        rate_of_rejection = self.test_array[statistic]

        if (rate_of_rejection==1.0): output = 1.0
        elif (rate_of_rejection==0.0): output = 0.0
        elif (rate_of_rejection<=np.random.uniform()):
            output = 1.0
        else:
            output = 0.0

        return [output, statistic]


class SimpleFiniteConfidence(Test):
    def __init__(self, pi_0, phi, epsilon, delta):
        self.order = len(pi_0)
        self.epsilon = epsilon
        self.delta = delta
        self.pi_0 = pi_0
        self.phi = phi

    def get_sample_num(self):
        return self.order/np.power(self.epsilon,2.0) * np.log(self.order/self.delta)

    def test(self, data):
        phi_estimate = ranking_utils.getMallowsParameterEstimator( data, self.pi_0 )
        if (np.abs(phi_estimate-self.phi) > self.epsilon):
            return 1
        else:
            return 0

if __name__ == "__main__":
    M =5
    test = SimpleFiniteSample(range(1,M+1), 0.2, 0.05, 10)

    print(test.test)