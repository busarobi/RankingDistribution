import numpy as np
import matplotlib.pyplot as plt
import os

def samp_comp(arr, gamma, delta):
    ret = []
    for m in arr:
        val = 1.0/gamma * np.log(m/delta)
        ret.append(val)
    return ret


m_arr = range(5,1000)
gamma_arr = [0.01, 0.05, 0.1]
colot = ['b', 'k', 'r']
delta = 0.05
for gamma, c in zip(gamma_arr, colot):
    plt.plot(m_arr,samp_comp(m_arr, gamma, delta), color=c,linewidth=2.0, linestyle='--', label="$\gamma = %g$" % gamma )

plt.legend(loc=1)
plt.grid()
plt.xlabel("$m$", fontsize=20)
plt.ylabel("Sample complexity", fontsize=20)
#plt.show()


from matplotlib.backends.backend_pdf import PdfPages
plt.tight_layout()

pdffile = '/Users/busafekete/Dropbox/Apps/Overleaf/2018-RankHyp/testingMallows/figs/central_ranking.pdf'
print(pdffile)
pp = PdfPages(pdffile)
plt.savefig(pp, format='pdf')
pp.close()
plt.close()
