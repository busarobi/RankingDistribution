import numpy as np
#import statsmodels
import itertools
import os

def getSampleFromMallows(model):
    return []


def normalizationMallows(M, phi):
    ret_val=1.0
    for i1 in range(1,M):
        tmp_sum = 0.0
        for i2 in range(0,i1+1):
            tmp_sum += np.power(phi,i2)

        ret_val *= tmp_sum
    return ret_val


def expectedSufficientStatMallows(M, phi):
    theta = np.log(phi)
    ret_val=0.0
    for i1 in range(1,M):
        tmp_sum_enum = 0.0
        tmp_sum_denum = 0.0
        for i2 in range(0,i1+1):
            tmp_sum_enum += (i2*np.exp(theta*i2))
            tmp_sum_denum += np.exp(theta * i2)

        ret_val += (tmp_sum_enum/tmp_sum_denum)
    return ret_val

# def expectedSufficientStatMallows(M, phi):
#     theta = np.log(phi)
#     ret_val=0.0
#     for i1 in range(1,M):
#         tmp_sum_enum = 0.0
#         for i2 in range(1,i1+1):
#             tmp_sum_enum += (i2*np.exp(theta*(i2-1)))
#
#         ret_val += tmp_sum_enum
#     return ret_val

# convert ordering to ranking for example the ordering is 3 4 2 6 1 5
def order2ranking(order):
    l = len(order)
    ranking = np.zeros((l,))
    for i in range(l):
        o = order[i]
        ranking[o-1] = i+1

    return ranking


def kendall_tau(ranking1, ranking2):
    distance = 0
    for x, y in itertools.combinations(range(0, len(ranking1)), 2):
        a = ranking1[x] - ranking1[y]
        b = ranking2[x] - ranking2[y]
        # if discordant (different signs)
        if (a * b < 0):
            distance += 1
    return distance

def kendall_tau_norm(ranking1, ranking2):
     return kendall_tau(ranking1,ranking2) / (len(ranking1) * (len(ranking1)-1.0) /2.0 )




def binarySearchMallows(M, s, lb, ub, err=10e-7):
    phi_estimate = (lb+ub)/2.0
    v = expectedSufficientStatMallows(M, phi_estimate)
    if (np.abs(v-s)<err):
        return phi_estimate
    if (v<s):
        return binarySearchMallows(M,s,phi_estimate,ub,err)
    else:
        return binarySearchMallows(M,s,lb,phi_estimate, err)

def getMallowsParameterEstimator( rankings, central_ranking ):
    s = 0.0
    M = len(rankings[0])
    for r in rankings:
        s = s+kendall_tau(central_ranking, r)

    s = s / len(rankings) # sufficient stat

    phi_estimate = binarySearchMallows(M, s, 0.0, 1.0 )
    return phi_estimate