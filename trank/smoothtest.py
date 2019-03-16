import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from scipy.stats import distributions
from collections import namedtuple

########################################################################################################################
## Neyman smooth-type test for multinomial data
#
# @article{Eub97,
# 	Author = {R. L. Eubank},
# 	Journal = {Journal of the American Statistical Association},
# 	Number = {439},
# 	Pages = {1084--1093},
# 	Title = {Testing Goodness of Fit with Multinomial Data},
# 	Volume = {92},
# 	Year = {1997}}
########################################################################################################################
########################################################################################################################


def get_basis_uniform(M):
    basis = np.zeros((M,M))
    fM = float(M)
    for i1 in range(M-1):
        for i2 in range(M):
            basis[i1,i2] = np.sqrt(2.0/fM)*np.cos(((i1+1)*np.pi*(i2+0.5))/fM)
    basis[M-1,:] = 1/fM

    return basis

# terms of \chi^2 statistic
def getf(p0, p_emp):
    return (p_emp-p0) / np.sqrt(p0)


# Fourier coefficients
def getb(fhat, basis):
    M = len(fhat)
    bs = np.zeros((M,))
    for i1 in range(M):
        bs[i1] = np.dot(basis[i1,:], fhat)
    return bs

def getvjj(j, p_emp, p0, basis):
    vjj = 0
    order = len(p0)
    for i1 in range(order):
        vjj += (basis[j,i1] * basis[j,i1] * p_emp[i1]) / p0[i1]

    return vjj

Power_divergenceResult = namedtuple('Power_divergenceResult',
                                    ('statistic', 'pvalue'))

def Neyman_smooth_test_foruniform(obs):
    num_of_obs = np.sum(obs)
    p_emp = obs / float(num_of_obs)
    order = len(obs)

    p0 = np.zeros((order,))
    p0[:] = 1 / float(order)

    basis = get_basis_uniform(order)
    fhat = getf(p0, p_emp)
    bs = getb(fhat, basis)

    # order selection accprdomg to Eq. (15)
    #chisquares = np.zeros((order-1,))
    Mhat = np.zeros((order,))
    #chisquares[0] = num_of_obs * bs[0] * bs[0]
    Mhat[1] = ((num_of_obs+1.0) / (num_of_obs-1.0)) * (bs[0] * bs[0]) - (2.0 / (num_of_obs - 1.0)) * getvjj( 0, p_emp, p0, basis)
    for i1 in range(1,order-1):
        #chisquares[i1] = chisquares[i1-1] + num_of_obs * bs[i1] * bs[i1]
        Mhat[i1+1] = Mhat[i1] + ((num_of_obs+1.0) / (num_of_obs-1.0)) * (bs[i1] * bs[i1]) - (2.0 / (num_of_obs - 1.0)) * getvjj( i1, p_emp, p0, basis)


    q = np.argmax(Mhat)
    if Mhat[q]<0:
        q = 0
    print( "\t --> Order of the test: %d" % (q))
    print("\t --> Mhat: %s"% (["".join("%s" % m)for m in Mhat]))


    stat = 0
    for i1 in range(q):
        stat += num_of_obs * (bs[0] * bs[0])

    print( "\t --> stat: %f" % stat)
    p = distributions.chi2.sf(stat, 1)
    return Power_divergenceResult(stat, p)

if __name__ == "__main__":

    testcase = "smallpert"
    M=10
    m = get_basis_uniform(M)
    print(m)
    # print(np.sum(m[0,:]))
    # print(np.dot(m[0,:], m[1,:]))
    # for i1 in range(M - 1):
    #     for i2 in range(M):
    #         print("%.20f " % m[i1,i2])
    #
    #     print

    p0 = np.zeros((M,))
    p0[:] = 1/float(M)

    print( "null hyp")
    print(p0)

    p_alternative = np.zeros((M,))
    if testcase == "smallpert":
        p_alternative[:] = 1/float(M)
        p_alternative[M-1] -= 1/(3.*float(M))
        p_alternative[M-2] += 1/(3.*float(M))
    elif testcase == "harmonic":
        for i1 in range(M):
            p_alternative[i1] = 1 / float(M) + 0.01 * np.cos(((i1 + 1) * np.pi * (i1 + 1 / 2)) / float(M))

    #p_emp = p_emp / np.sum(p_emp)
    print( "True distribution")
    print(p_alternative)

    # fhat = getf(p0, p_emp)
    # print(fhat)
    # bs = getb(fhat,m)
    # print( "Fourier coeffs")
    # print(bs)
    # for idx in range(M):
    #     lab = "$%d$" % (idx+1)
    #     plt.plot(range(1,M+1),m[idx,:], label=lab)
    #
    #
    # plt.grid(True)
    # plt.legend()
    # plt.show()


    # chisquare([16, 18, 16, 14, 12, 12], f_exp=[16, 16, 16, 16, 16, 8])

    rep = 100
    parr = []
    for i in range(rep):
        obs = np.random.multinomial(1000, p_alternative)
        print("Empricial")
        print(obs / float(np.sum(obs)))

        resNeyman = Neyman_smooth_test_foruniform(obs)
        res = chisquare(obs)

        parr.append((resNeyman,res))


    for i in range(rep):
        print("p-value: %.7f\t %.7f" % (parr[i][0].pvalue, parr[i][1].pvalue))
        print("Stat   : %.7f\t %.7f" % (parr[i][0].statistic, parr[i][1].statistic))