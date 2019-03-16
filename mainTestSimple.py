from trank import Mallows, Mahonian
from trank import ranking_utils
import numpy as np
import matplotlib.pyplot as plt

m=5
pi0 = range(1,m+1)
n=5000
phi=0.2
repetitions = 100
model = Mallows(pi0, phi)
eval = ranking_utils.expectedSufficientStatMallows(m,phi)

mahonian = Mahonian(m)
print(mahonian.get(m - 3))
print(mahonian.getArray())

stats = np.zeros((repetitions,))
for l in xrange(repetitions):
    data = np.zeros((n,))
    rankings = []
    for i in xrange(n):
        r = model.get_sample()
        rankings.append(r)
        data[i] = ranking_utils.kendall_tau(pi0, r)
        stats[l] = np.sum(data)
    phi_est = ranking_utils.getMallowsParameterEstimator(rankings, pi0)
    print("Stat: %f, (%f) Param estimate: %f (%f)" % (stats[l]/n, eval, phi_est , phi) )
#
# n, bins, patches = plt.hist(x=stats, bins=30, color='#0504aa', alpha=0.7, rwidth=0.85)
# plt.show()