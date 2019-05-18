from trank import Mallows, Mahonian
from trank import ranking_utils
import numpy as np
import matplotlib.pyplot as plt
from trank.test_simple import SimpleFixedSample, SimpleFixedConfidence
m=15
pi0 = range(1,m+1)
n=100
phi=0.9
alpha = 0.05
repetitions = 100
model = Mallows(pi0, phi)
epsilon = 0.1

test_fixed_sample = SimpleFixedSample(pi0, phi,alpha,n)
test_fixed_confidence = SimpleFixedConfidence(pi0, phi, alpha, epsilon, 0.0, debug=True)

print(test_fixed_sample.to_string())
sampcomp = test_fixed_confidence.get_sample_num()
print("samp comp: %d" % (sampcomp))

# testing the test when null hyp is true
rejection_fixed_sample = np.zeros((repetitions,))
stats_fixed_sample = np.zeros((repetitions,))
power_fixed_sample = 0.0

rejection_fixed_confidence = np.zeros((repetitions,))
stats_fixed_confidence = np.zeros((repetitions,))
power_fixed_confidence = 0.0

for l in xrange(repetitions):
    ############ fixed sample
    rankings = []

    for i in xrange(n):
        r = model.get_sample()
        rankings.append(r)

    [rejection_fixed_sample[l], stats_fixed_sample[l]] = test_fixed_sample.test(rankings)
    #print(l, rejection[l], stats[l])
    if ( rejection_fixed_sample[l]>0.0):
        #
        power_fixed_sample += 1.0

    ############ fixed confidence
    rankings = []
    for i in xrange(sampcomp):
        r = model.get_sample()
        rankings.append(r)

    rejection_fixed_confidence[l] = test_fixed_confidence.test(rankings)
    #print(l, rejection[l], stats[l])
    if ( rejection_fixed_confidence[l]>0.0):
        #
        power_fixed_confidence += 1.0



print("Power: %f" % (power_fixed_sample/repetitions))
print("Power: %f" % (power_fixed_confidence/repetitions))






    #phi_est = ranking_utils.getMallowsParameterEstimator(rankings, pi0)
    #print("Stat: %f, (%f) Param estimate: %f (%f)" % (stats[l]/n, eval, phi_est , phi) )
#
# n, bins, patches = plt.hist(x=stats, bins=30, color='#0504aa', alpha=0.7, rwidth=0.85)
# plt.show()