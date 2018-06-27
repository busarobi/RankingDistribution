import numpy as np
import statsmodels
import itertools

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
