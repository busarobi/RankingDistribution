from trank import Mallows, Mahonian
from trank import ranking_utils
import numpy as np
import matplotlib.pyplot as plt
from trank.test_simple import SimpleFixedSample, SimpleFixedConfidence


def get_power(test, m, repetitions):
    rejection = np.zeros((repetitions,))
    stats = np.zeros((repetitions,))
    power = 0.0

    for l in xrange(repetitions):
        ############ fixed sample
        rankings = []

        for i in xrange(n):
            r = m.get_sample()
            rankings.append(r)

        [rejection[l], stats[l]] = test.test(rankings)
        # print(l, rejection[l], stats[l])
        if (rejection[l] > 0.0):
            #
            power += 1.0
    power = (power / repetitions)
    #print("Power: %f" % power)
    return power


def save_power_curve(phi_arr, power_arr, phi0, m, n, alpha, rep):
    fname = "results/res_phi0_%g_m_%d_n_%d_alpha_%g_rep_%d_power" % (phi0, m, n, alpha, rep)
    fname = fname.replace(".","_") + ".txt"
    print("Save to : %s" % (fname))
    with open(fname,"w") as f:
        for [phi,p] in zip(phi_arr,power_arr):
            f.write("%f,%f\n" % (phi,p))
    f.close()

m=15
pi0 = range(1,m+1)
n=50
phi0=0.5
alpha = 0.05
repetitions = 100

power_arr = []
phi_arr = []

test_fixed_sample = SimpleFixedSample(pi0, phi0,alpha,n)
print(test_fixed_sample.to_string())

# right
test_anymore = True
for phi in np.arange(phi0,1.0,0.01):
    if (test_anymore):
        model = Mallows(pi0, phi)
        power = get_power(test_fixed_sample, model, repetitions)
        print("phi: %f\tphi_0: %f\tpower: %f" % (phi, phi0, power))
    else:
        power = 1.0

    phi_arr.append(phi)
    power_arr.append(power)

    if (power>0.99):
        test_anymore = False


# left
test_anymore = True
for phi in np.arange(phi0,0.0,-0.01):
    if (test_anymore):
        model = Mallows(pi0, phi)
        power = get_power(test_fixed_sample, model, repetitions)
        print("phi: %f\tphi_0: %f\tpower: %f" % (phi, phi0, power))
    else:
        power = 1.0
    phi_arr.insert(0,phi)
    power_arr.insert(0,power)

    if (power>0.99):
        test_anymore = False

save_power_curve(phi_arr,power_arr,phi0, m, n, alpha, repetitions)


