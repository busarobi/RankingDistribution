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
    ax = fig.add_subplot(2, 1, 1)

    epsilon = 0.05
    [phi_arr, power_arr, noanswer_arr] = get_power_curve_fc(phi0, m, delta, epsilon0, epsilon, repetitions)
    ax.plot(phi_arr,power_arr, color="b",linewidth=3.0, label="$(\epsilon = %g $)" % epsilon )
    #ax.plot(phi_arr,noanswer_arr, color="b",linewidth=5.0, label="" , linestyle='-.' )

    epsilon = 0.01
    [phi_arr, power_arr, noanswer_arr] = get_power_curve_fc(phi0, m, delta, epsilon0, epsilon, repetitions)
    ax.plot(phi_arr,power_arr, color="r",linewidth=3.0, label="$(\epsilon = %g $)" % epsilon )
    #ax.plot(phi_arr,noanswer_arr, color="r",linewidth=5.0, label="" , linestyle='-.' )

    # ax.plot([phi0-epsilon0,phi0-epsilon0],[0,1], color="b", linewidth=2.0, label="", linestyle='--')
    # ax.plot([phi0+epsilon0,phi0+epsilon0],[0,1], color="b", linewidth=2.0, label="", linestyle='--')
    fancy = mpatches.FancyBboxPatch([phi0-epsilon0, 0.0], 2*epsilon0, 1.0, alpha=0.3, color="g",
                                    boxstyle=mpatches.BoxStyle("Round", pad=0.0), label="$H_0$")
    ax.add_patch(fancy)

    plt.rcParams.update({'font.size': 18})
    plt.grid()
    if (loopi==1):
        plt.legend(loc=5, fontsize=15)
    loopi += 1
    plt.xlabel("$\phi$", fontsize=30)
    plt.ylabel("Power", fontsize=25)
    #plt.show()
    plt.xlim([np.max([0.0, phi0-0.15]),np.min([phi0+0.15, 1.0])])
    plt.ylim([-0.01,1.01])



    ax = fig.add_subplot(2, 1, 2)

    epsilon = 0.05
    [phi_arr, power_arr, noanswer_arr] = get_power_curve_fc(phi0, m, delta, epsilon0, epsilon, repetitions)
    #ax.plot(phi_arr,power_arr, color="b",linewidth=5.0, label="Power $(\epsilon = %g $)" % epsilon )
    ax.plot(phi_arr,noanswer_arr, color="b",linewidth=3.0, label="" )

    epsilon = 0.01
    [phi_arr, power_arr, noanswer_arr] = get_power_curve_fc(phi0, m, delta, epsilon0, epsilon, repetitions)
    #ax.plot(phi_arr,power_arr, color="r",linewidth=5.0, label="Power $(\epsilon = %g $)" % epsilon )
    ax.plot(phi_arr,noanswer_arr, color="r",linewidth=3.0, label=""  )

    # ax.plot([phi0-epsilon0,phi0-epsilon0],[0,1], color="b", linewidth=2.0, label="", linestyle='--')
    # ax.plot([phi0+epsilon0,phi0+epsilon0],[0,1], color="b", linewidth=2.0, label="", linestyle='--')
    fancy = mpatches.FancyBboxPatch([phi0-epsilon0, 0.0], 2*epsilon0, 1.0, alpha=0.3, color="g",
                                    boxstyle=mpatches.BoxStyle("Round", pad=0.0), label="$H_0$")
    ax.add_patch(fancy)

    plt.rcParams.update({'font.size': 22})
    plt.grid()
    if (loopi==1):
        plt.legend(loc=4)
    loopi += 1
    plt.xlabel("$\phi$", fontsize=30)
    plt.ylabel("No answer", fontsize=25)
    #plt.show()
    plt.xlim([np.max([0.0, phi0-0.15]),np.min([phi0+0.15, 1.0])])
    plt.ylim([-0.01,1.01])



    from matplotlib.backends.backend_pdf import PdfPages
    plt.tight_layout()
    # plt.show()
    pdf_fanme =  '/Users/busafekete/Dropbox/Apps/Overleaf/2018-RankHyp/testingMallows/figs/finite_conf_%g' % phi0
    pdf_fanme = pdf_fanme.replace(".", "_")
    pdf_fanme = pdf_fanme + ".pdf"
    print(pdf_fanme)
    pp = PdfPages( pdf_fanme )
    plt.savefig(pp, format='pdf')
    pp.close()
    plt.close()
