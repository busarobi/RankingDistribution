import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def get_power_curve(phi0, m, n, alpha, rep):
    fname = "results/res_phi0_%g_m_%d_n_%d_alpha_%g_rep_%d_power" % (phi0, m, n, alpha, rep)
    fname = fname.replace(".","_") + ".txt"
    print("Load : %s" % (fname))
    power_arr = []
    phi_arr = []

    with open(fname,"r") as f:
        for line in f:
            phi_arr.append(float(line.split(",")[0]))
            power_arr.append(float(line.split(",")[1]))

    f.close()
    return phi_arr, power_arr


def get_power_curve_fc(phi0, m, delta, epsilon0, epsilon, rep):
    fname = "results_2/fc_phi0_%g_m_%d_delta_%g_eps0_%g_eps_%g_rep_%d_power" % (phi0, m, delta, epsilon0, epsilon, rep)
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


loopi = 1
for phi0 in [0.1, 0.5, 0.9]:
    m=10
    pi0 = range(1,m+1)

    delta = 0.05
    alpha = delta
    repetitions = 20

    epsilon0 = 0.05


    col_arr = ["b", "r"]


    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    epsilon = 0.05
    [phi_arr, power_arr, noanswer_arr] = get_power_curve_fc(phi0, m, delta, epsilon0, epsilon, repetitions)
    ax.plot(phi_arr,power_arr, color="b",linewidth=5.0, label="Power $(\epsilon = %g $)" % epsilon )
    ax.plot(phi_arr,noanswer_arr, color="b",linewidth=5.0, label="" , linestyle='-.' )

    epsilon = 0.01
    [phi_arr, power_arr, noanswer_arr] = get_power_curve_fc(phi0, m, delta, epsilon0, epsilon, repetitions)
    ax.plot(phi_arr,power_arr, color="r",linewidth=5.0, label="Power $(\epsilon = %g $)" % epsilon )
    ax.plot(phi_arr,noanswer_arr, color="r",linewidth=5.0, label="" , linestyle='-.' )

    # ax.plot([phi0-epsilon0,phi0-epsilon0],[0,1], color="b", linewidth=2.0, label="", linestyle='--')
    # ax.plot([phi0+epsilon0,phi0+epsilon0],[0,1], color="b", linewidth=2.0, label="", linestyle='--')
    fancy = mpatches.FancyBboxPatch([phi0-epsilon0, 0.0], 2*epsilon0, 1.0, alpha=0.3, color="g",
                                    boxstyle=mpatches.BoxStyle("Round", pad=0.0), label="$H_0$")
    ax.add_patch(fancy)


    # phi0=0.45
    # n = 50
    # [phi_arr, power_arr] = get_power_curve(phi0, m, n, alpha, repetitions)
    # plt.plot(phi_arr,power_arr, color="k",linewidth=2.0, label=("$m=%d, n=%d, \phi_0=%g$"%(m,n,phi0)) )
    # plt.plot([phi0,phi0],[0,1], color="k", linewidth=2.0, label="")
    #
    # phi0=0.55
    # n = 50
    # [phi_arr, power_arr] = get_power_curve(phi0, m, n, alpha, repetitions)
    # plt.plot(phi_arr,power_arr, color="c",linewidth=2.0, label=("$m=%d, n=%d, \phi_0=%g$"%(m,n,phi0)) )
    # plt.plot([phi0,phi0],[0,1], color="c", linewidth=2.0, label="")


    # plt.text(phi0 - epsilon0, 0.9, "null", bbox={'facecolor':'red', 'alpha':0.5, 'pad':10}, size=20,
    #          horizontalalignment='center', verticalalignment='center')


    # plt.text(0.008, alpha+0.015, ("Significance level ($%g$)" % alpha), bbox=dict(facecolor='red'))
    # plt.plot([0,1],[alpha,alpha], color="k", linewidth=2.0)

    plt.rcParams.update({'font.size': 22})
    plt.grid()
    if (loopi==1):
        plt.legend(loc=4)
    loopi += 1
    plt.xlabel("$\phi$", fontsize=30)
    #plt.ylabel("Power", fontsize=25)
    #plt.show()
    plt.xlim([np.max([0.0, phi0-0.2]),np.min([phi0+0.2, 1.0])])
    plt.ylim([-0.01,1.01])

    from matplotlib.backends.backend_pdf import PdfPages
    plt.tight_layout()
    # plt.show()
    pdf_fanme =  '/Users/busafekete/Dropbox/Apps/Overleaf/2018-RankHyp/testingMallows/figs/finite_conf_%g' % phi0
    pdf_fanme = pdf_fanme.replace(".", "_")
    pp = PdfPages( pdf_fanme + ".pdf")
    plt.savefig(pp, format='pdf')
    pp.close()
    plt.close()
