import numpy as np
import matplotlib.pyplot as plt
import os


def get_power_curve(phi0, m, n, alpha, rep):
    fname = "results/res_phi0_%g_m_%d_n_%d_alpha_%g_rep_%d_power" % (phi0, m, n, alpha, rep)
    fname = fname.replace(".","_") + ".txt"
    print("Load : %s" % (fname))

    power_arr = []
    phi_arr = []
    if (os.path.isfile(fname)):
        with open(fname,"r") as f:
            for line in f:
                phi_arr.append(float(line.split(",")[0]))
                power_arr.append(float(line.split(",")[1]))

        f.close()
    return phi_arr, power_arr

def get_power_curve_no_central(phi0, m, n, alpha, rep):
    fname = "results/res_nc_phi0_%g_m_%d_n_%d_alpha_%g_rep_%d_power" % (phi0, m, 2*n, alpha, rep)
    fname = fname.replace(".","_") + ".txt"
    print("Load : %s" % (fname))

    power_arr = []
    phi_arr = []
    if (os.path.isfile(fname)):
        with open(fname,"r") as f:
            for line in f:
                phi_arr.append(float(line.split(",")[0]))
                power_arr.append(float(line.split(",")[1]))

        f.close()
    return phi_arr, power_arr


for m in [8,10,15]:
#for m in [8]:
    pi0 = range(1,m+1)
    n=50
    alpha = 0.05
    repetitions = 100

    col_arr = ["b", "r"]


    phi0=0.1
    [phi_arr, power_arr] = get_power_curve(phi0, m, n, alpha, repetitions)
    if (len(phi_arr) > 0):
        plt.plot(phi_arr,power_arr, color="b",linewidth=2.0, label=("$\phi_0=%g$"%(phi0)) )
        plt.plot([phi0,phi0],[0,1], color="b", linewidth=2.0, label="")

    [phi_arr, power_arr] = get_power_curve_no_central(phi0, m, n, alpha, repetitions)
    if (len(phi_arr) > 0):
        plt.plot(phi_arr,power_arr, color="b",linewidth=2.0, linestyle='--' )



    phi0=0.5
    [phi_arr, power_arr] = get_power_curve(phi0, m, n, alpha, repetitions)
    if (len(phi_arr) > 0):
        plt.plot(phi_arr,power_arr, color="g",linewidth=2.0, label=("$\phi_0=%g$"%(phi0)) )
        plt.plot([phi0,phi0],[0,1], color="g", linewidth=2.0, label="")
    [phi_arr, power_arr] = get_power_curve_no_central(phi0, m, n, alpha, repetitions)
    if (len(phi_arr) > 0):
        plt.plot(phi_arr,power_arr, color="g",linewidth=2.0,  linestyle='--' )


    phi0=0.9
    [phi_arr, power_arr] = get_power_curve(phi0, m, n, alpha, repetitions)
    if (len(phi_arr)>0):
        plt.plot(phi_arr,power_arr, color="r",linewidth=2.0, label=("$\phi_0=%g$"%(phi0)) )
        plt.plot([phi0,phi0],[0,1], color="r", linewidth=2.0, label="")
    else:
        plt.plot([0,0], [0,0], color="r", linewidth=2.0, label=("$\phi_0=%g$" % (phi0)))


    [phi_arr, power_arr] = get_power_curve_no_central(phi0, m, n, alpha, repetitions)
    if (len(phi_arr)>0):
        plt.plot(phi_arr,power_arr, color="r",linewidth=2.0, linestyle='--' )


    plt.text(0.006, 0.016, ("Significance level ($\\alpha=%g$)" % alpha), bbox=dict(facecolor='red'))
    plt.plot([0,1],[alpha,alpha], color="k", linewidth=2.0)

    plt.rcParams.update({'font.size': 13})
    plt.grid()
    plt.title("$m=%d$"%m)
    if (m==15):
        plt.legend()
    plt.xlabel("$\phi$", fontsize=20)
    plt.ylabel("Power", fontsize=20)
    #plt.show()


    from matplotlib.backends.backend_pdf import PdfPages
    plt.tight_layout()

    pdffile = '/Users/busafekete/Dropbox/Apps/Overleaf/2018-RankHyp/testingMallows/figs/finite_sample_m_%d.pdf' % (m)
    print(pdffile)
    pp = PdfPages(pdffile)
    plt.savefig(pp, format='pdf')
    pp.close()
    plt.close()
