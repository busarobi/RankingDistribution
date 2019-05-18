import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def get_power_curve_fc(phi0, m, delta, epsilon0, epsilon, rep):
    fname = "results/fc_phi0_%g_m_%d_delta_%g_eps0_%g_eps_%g_rep_%d_power" % (phi0, m, delta, epsilon0, epsilon, rep)
    fname = fname.replace(".","_") + ".txt"

    print("Load : %s" % (fname))
    power_arr = []
    phi_arr = []
    noanswer_arr = []

    with open(fname,"r") as f:
        for line in f:
            phi_arr.append(float(line.split(",")[0]))
            power_arr.append(float(line.split(",")[1]))
            noanswer_arr.append(float(line.split(",")[2]))

    f.close()
    return phi_arr, power_arr, noanswer_arr


m=5
pi0 = range(1,m+1)
phi0=0.5
delta = 0.05
repetitions = 100

epsilon0 = 0.05
epsilon = 0.05

col_arr = ["b", "r"]


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

[phi_arr, power_arr, noanswer_arr] = get_power_curve_fc(phi0, m, delta, epsilon0, epsilon, repetitions)
ax.plot(phi_arr,power_arr, color="b",linewidth=5.0, label="Power of FC" )
ax.plot(phi_arr,noanswer_arr, color="b",linewidth=5.0, label="Decision rate of FC" , linestyle='-.' )

epsilon = 0.01
[phi_arr, power_arr, noanswer_arr] = get_power_curve_fc(phi0, m, delta, epsilon0, epsilon, repetitions)
ax.plot(phi_arr,power_arr, color="r",linewidth=5.0, label="Power of FC" )
ax.plot(phi_arr,noanswer_arr, color="r",linewidth=5.0, label="Decision rate of FC" , linestyle='-.' )

# ax.plot([phi0-epsilon0,phi0-epsilon0],[0,1], color="b", linewidth=2.0, label="", linestyle='--')
# ax.plot([phi0+epsilon0,phi0+epsilon0],[0,1], color="b", linewidth=2.0, label="", linestyle='--')
fancy = mpatches.FancyBboxPatch([phi0-epsilon0, 0.0], 2*epsilon0, 1.0, alpha=0.3, color="g",
                                boxstyle=mpatches.BoxStyle("Round", pad=0.0), label="$H_0$")
ax.add_patch(fancy)

# plt.text(phi0 - epsilon0, 0.9, "null", bbox={'facecolor':'red', 'alpha':0.5, 'pad':10}, size=20,
#          horizontalalignment='center', verticalalignment='center')


plt.grid()
plt.legend()
plt.xlabel("$\phi$", fontsize=25)
#plt.ylabel("Power", fontsize=25)
#plt.show()
plt.xlim([0.3,0.7])
plt.ylim([-0.01,1.01])

from matplotlib.backends.backend_pdf import PdfPages
plt.tight_layout()
# plt.show()

pp = PdfPages('/Users/busafekete/Dropbox/Apps/Overleaf/2018-RankHyp/testingMallows/figs/finite_conf_1.pdf')
plt.savefig(pp, format='pdf')
pp.close()
plt.close()
