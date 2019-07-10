from trank import Mallows, Mahonian
from trank import ranking_utils
import numpy as np
import matplotlib.pyplot as plt
from trank.test_simple import SimpleFixedSample, SimpleFixedConfidence
m=15
pi0 = range(1,m+1)
phi=0.9
alpha = 0.05
repetitions = 100
model = Mallows(pi0, phi)
epsilon = 0.025

test_fixed_confidence = SimpleFixedConfidence(pi0, phi, alpha, epsilon, 0.0, debug=True)

sampcomp = test_fixed_confidence.get_sample_num()
print("samp comp: %d" % (sampcomp))

# rejection_fixed_confidence = np.zeros((repetitions,))
# stats_fixed_confidence = np.zeros((repetitions,))
# power_fixed_confidence = 0.0
#
# for l in xrange(repetitions):
#     ############ fixed sample
#     rankings = []
#
#     for i in xrange(n):
#         r = model.get_sample()
#         rankings.append(r)
#
#
#     ############ fixed confidence
#     rankings = []
#     for i in xrange(sampcomp):
#         r = model.get_sample()
#         rankings.append(r)
#
#     rejection_fixed_confidence[l] = test_fixed_confidence.test(rankings)
#     #print(l, rejection[l], stats[l])
#     if ( rejection_fixed_confidence[l]>0.0):
#         #
#         power_fixed_confidence += 1.0
#
#
#
# print("Power: %f" % (power_fixed_confidence/repetitions))



