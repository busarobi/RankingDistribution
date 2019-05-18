from testown import TestOwn
from partition_number import Partition, SufficientStatisticDistribution
from mallows_model import Mallows
import numpy as np
from trank import ranking_utils


class SimpleFixedSample(TestOwn):
    def __init__(self, pi_0, phi, alpha, sample_size, approx=True, central_ranking_known = True):
        self.order = len(pi_0)
        self.alpha = alpha
        self.sampe_size = sample_size

        self.mallows = Mallows(pi_0, phi)
        self.central_ranking_known = central_ranking_known

        if (self.central_ranking_known == False): # take hal of the sample to estimate the central ranking
            self.sampe_size_full = self.sampe_size
            self.sampe_size = int(round(self.sampe_size/2))



        self.approx = approx
        self.phi = phi
        print( "Generating partition numbers...")
        if (self.approx):
            self.partition = SufficientStatisticDistribution(self.order, self.sampe_size, self.phi)
        else:
            self.partition = Partition(self.order, self.sampe_size)

        print("Done.")


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
        print(np.abs((1.0-power)-alpha))
        assert(np.abs((1.0-power)-alpha)<10e-3)

    def get_probability_of_stat(self, l):
        if (self.approx):
            frac = self.partition.get(l)
        else:
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
        if self.central_ranking_known:
            s = np.zeros((self.sampe_size,))
            for i, r in enumerate(data):
                s[i] = ranking_utils.kendall_tau(self.mallows.central_ranking, r)
        else:
            avg_rankings = np.zeros((self.mallows.order,))
            self.sampe_size
            for i in range(self.sampe_size+1, self.sampe_size_full):
                for i, r in enumerate(data[i]):
                    avg_rankings[r-1] += i

            pi = np.argsort(avg_rankings)+1
            pi = ranking_utils.order2ranking(pi)
            #print(pi)
            s = np.zeros((self.sampe_size,))
            for i in range(self.sampe_size):
                s[i] = ranking_utils.kendall_tau(pi, ranking_utils.order2ranking(data[i]))

        statistic = np.sum(s)
        rate_of_rejection = self.test_array[statistic]

        if (rate_of_rejection==1.0): output = 1.0
        elif (rate_of_rejection==0.0): output = 0.0
        elif (rate_of_rejection<=np.random.uniform()):
            output = 1.0
        else:
            output = 0.0

        return [output, statistic]


class SimpleFixedConfidence(TestOwn):
    def __init__(self, pi_0, phi, delta, epsilon0, epsilon, debug = False): # delta is eqivalent to alpha in the fixed sample case
        self.order = len(pi_0)
        self.epsilon = epsilon
        self.epsilon0 = epsilon0
        self.delta = delta
        self.pi_0 = pi_0
        self.phi = phi
        self.debug = debug

    def get_sample_num(self):
        return int(np.floor(self.order/np.power(self.epsilon0,2.0) * np.log(self.order/self.delta)))

    def test(self, data):
        phi_estimate = ranking_utils.getMallowsParameterEstimator( data, self.pi_0 )

        if (self.debug):
            print( "--> phi_0 -+eps: [%g, %g], phi estimate: %g" % (self.phi -self.epsilon0, self.phi +self.epsilon0, phi_estimate))

        if (np.abs(phi_estimate-self.phi) < self.epsilon0):
            if (self.debug):
                print( "--> Accept")
            return 0
        else:
            if (phi_estimate > self.phi + self.epsilon0):
                threshold = (np.sqrt(self.order) / 4.0) * np.log(phi_estimate/(self.phi + self.epsilon0))
                if (threshold>self.epsilon):
                    if (self.debug):
                        print("--> Reject (bigger), threshold: %g, epsilon: %g" % (threshold, self.epsilon))
                    return 1
                else:
                    if (self.debug):
                        print("--> No answer      , threshold: %g, epsilon: %g" % (threshold, self.epsilon))
                    return -1

            if (phi_estimate < self.phi - self.epsilon0):
                threshold = (np.sqrt(self.order) / 4.0) * np.log((self.phi - self.epsilon0)/phi_estimate)
                if (threshold>self.epsilon):
                    if (self.debug):
                        print("--> Reject (smaller), threshold: %g, epsilon: %g" % (threshold, self.epsilon))
                    return 1
                else:
                    if (self.debug):
                        print("--> No answer      , threshold: %g, epsilon: %g" % (threshold, self.epsilon))
                return -1


if __name__ == "__main__":
    M =5
    test = SimpleFixedSample(range(1,M+1), 0.2, 0.05, 10)
    print(test.test)