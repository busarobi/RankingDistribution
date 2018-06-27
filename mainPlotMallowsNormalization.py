from utils import normalizationMallows
import numpy as np
import matplotlib.pyplot as plt

Mrange = range(3,10)
vmat = []
r = np.arange(0.001, 0.999, 0.01)
for M in Mrange:
    v = []
    for i1 in r:
        val = normalizationMallows(M, i1)
        v.append(val)

    v = np.asarray(v)
    vmat.append(v)


for idx, M in enumerate(Mrange):
    lab = "$M=%d$" % M
    plt.semilogy(r,vmat[idx], label=lab)


plt.ylabel('$Z( \phi )$ ')
plt.xlabel('$\phi$ ')
plt.grid(True)
plt.legend()
plt.show()

