from trank import Mallows, Mahonian
from trank import ranking_utils
import numpy as np
import matplotlib.pyplot as plt
from trank.test_simple import SimpleFiniteSample
m=5
pi0 = range(1,m+1)
n=50
phi=0.2
alpha = 0.05
repetitions = 500
model = Mallows(pi0, phi)

test = SimpleFiniteSample(pi0, phi,alpha,n)
print(test.to_string())


rejection = np.zeros((repetitions,))
stats = np.zeros((repetitions,))
power = 0.0
for l in xrange(repetitions):
    rankings = []

    for i in xrange(n):
        r = model.get_sample()
        rankings.append(r)


    [rejection[l], stats[l]] = test.test(rankings)
    #print(l, rejection[l], stats[l])
    if ( rejection[l]>0.0):
        #
        power += 1.0


print("Power: %f" % (power/repetitions))


    #phi_est = ranking_utils.getMallowsParameterEstimator(rankings, pi0)
    #print("Stat: %f, (%f) Param estimate: %f (%f)" % (stats[l]/n, eval, phi_est , phi) )
#
# n, bins, patches = plt.hist(x=stats, bins=30, color='#0504aa', alpha=0.7, rwidth=0.85)
# plt.show()