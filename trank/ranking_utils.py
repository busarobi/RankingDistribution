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


# convert ordering to ranking for example the ordering is 3 4 2 6 1 5
def order2ranking(order):
    l = len(order)
    ranking = np.zeros((l,))
    for i in range(l):
        o = order[i]
        ranking[o-1] = i+1

    return ranking


def kendall_tau(ranking1, ranking2):
    pairs = itertools.combinations(range(0, len(ranking1)), 2)

    distance = 0

    for x, y in pairs:
        a = ranking1[x] - ranking1[y]
        b = ranking2[x] - ranking2[y]

        # if discordant (different signs)
        if (a * b < 0):
            distance += 1

    return distance


# Python3 program to find number of permutation
# with K inversion using Memoization
# method recursively calculates
# permutation with K inversion
# 2D array memo for stopping
# solving same problem again
#memo = [[0 for i in range(100)] for j in range(100)]
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(memo=[[0 for i in range(100)] for j in range(100)])
def rec(N, K):

    # Base cases
    if (N == 0): return 0
    if (K == 0): return 1

    # If already solved then
    # return result directly
    if (rec.memo[N][K] != 0):
        return rec.memo[N][K]

    # Calling recursively all subproblem
    # of permutation size N - 1
    sum = 0
    for i in range(K + 1):

        # Call recursively only if
        # total inversion to be made
        # are less than size
        if (i <= N - 1):
            sum += rec(N - 1, K - i)

    # store result into memo
    rec.memo[N][K] = sum

    return sum

def numberOfPermWithKInversion(N, K):
    rec(N, K)
    if (K==0):
        return 1
    else:
        return rec.memo[N][K]


def getNumberOfPermWithKInversionArray(N):
    m = (N * (N - 1)) / 2 + 1
    arr = np.zeros((m,))

    fname = './trank/inversions/data_%d.txt'% N
    exists = os.path.isfile(fname)
    if exists:
        with open(fname, 'r') as f:
            for i, line in enumerate(f):
                arr[i]=int(line)
    else:
        arr[0]=1
        for i in xrange(1,m):
            rec(N, i)
            arr[i] = rec.memo[N][i]

        with open(fname, 'w') as f:
            for i in arr:
                f.write("%g\n" % i)
            f.close()

    return arr


def binarySearchMallows(M, s, lb, ub, err=10e-8):
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