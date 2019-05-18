import sys
sys.path.append('./trank/')

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm


if __name__ == '__main__':
    res = {}
    m_arr = set()
    phi_arr = set()

    fname = "./results/avg_rank_results.txt"
    with (open(fname, "r")) as f:
        for l in f:
            m = l.split(",")[0].split(":")[1]
            phi = l.split(",")[1].split(":")[1]

            m_arr.add(int(m))
            phi_arr.add(float(phi))
            n = []
            acc = []
            for tok in l.split(",")[2:]:
                n.append(int(tok.split(":")[0]))
                acc.append(float(tok.split(":")[1]))

            res[m+"_"+phi] = [n,acc]
    f.close()


    print(res)
    print(phi_arr)
    print(m_arr)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.grid()

    ms = [5,10,50]
    pr = [0.1, 0.5, 0.9]
    r=len(ms)*len(pr)
    x = np.arange(r)
    ys = [i + x + (i * x) ** 2 for i in range(r)]

    colors = cm.rainbow(np.linspace(0, 1, len(ys)))
    j = 0
    for i, m in enumerate(ms):
        n = 0
        for phi in pr:
            key = str(m) + "_" + str(phi)
            arrays = res[key]
            ax.semilogx(arrays[0], arrays[1], color=colors[j], linewidth=2.0, label="$m=%d, \phi=%g$" % (m,phi))
            # if (n == 0):
            #     ax.semilogx(arrays[0], arrays[1], color=colors[j], linewidth=2.0, label="m=%d" % (m))
            #     n+=1
            # else:
            #     ax.semilogx(arrays[0], arrays[1], color=colors[j], linewidth=2.0)
            j+=1
    plt.legend(loc=3,fontsize=20)

    plt.xlabel("Number of samples", fontsize=25)
    plt.ylabel("Accuracy", fontsize=25)
    print("")

    from matplotlib.backends.backend_pdf import PdfPages
    plt.tight_layout()

    pp = PdfPages('/Users/busafekete/Dropbox/Apps/Overleaf/2018-RankHyp/testingMallows/figs/finite_sample_2.pdf')
    plt.savefig(pp, format='pdf')
    pp.close()
    plt.close()
