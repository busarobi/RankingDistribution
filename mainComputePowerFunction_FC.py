import sys
sys.path.append('./trank/')

from trank import Mallows
import numpy as np
from trank.test_simple import SimpleFixedConfidence
import time
import multiprocessing


def worker(procnum, return_dict, pi0, phi, test):
    rankings = []
    m = Mallows(pi0, phi)
    for i in range(test.get_sample_num()):
        r = m.get_sample()
        rankings.append(r)

    rej = test.test(rankings)

    #print str(procnum) + ' represent!'
    return_dict[procnum] = rej


def get_power_parallel(test, pi0, phi, repetitions):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(repetitions):
        p = multiprocessing.Process(target=worker, args=(i, return_dict, pi0, phi, test))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    power = 0.0
    noanswer = 0.0
    for rejection in return_dict.values():
        if (rejection > 0.0):
            #
            power+= 1.0
        if (rejection < 0.0):
            noanswer += 1.0

    power = (power / repetitions)
    noanswer = (noanswer / repetitions)

    return power, noanswer


def get_power(test, m, repetitions):
    rejection = np.zeros((repetitions,))
    power = 0.0
    noanswer = 0.0
    for l in range(repetitions):
        ############ fixed confidence
        rankings = []
        for i in range(test.get_sample_num()):
            r = m.get_sample()
            rankings.append(r)

        rejection[l] = test.test(rankings)
        # print(l, rejection[l], stats[l])
        if (rejection[l] > 0.0):
            #
            power+= 1.0
        if (rejection[l] < 0.0):
            noanswer += 1.0

    if (noanswer == repetitions):
        power = 0.0
    else:
        power = (power / (repetitions-noanswer))
    noanswer = (noanswer / repetitions)
    #print("Power: %f" % power)
    return power, noanswer


def save_power_curve(phi_arr, power_arr, noanswer_arr, phi0, m, delta, epsilon0, epsilon, rep):
    fname = "results_2/fc_phi0_%g_m_%d_delta_%g_eps0_%g_eps_%g_rep_%d_power" % (phi0, m, delta, epsilon0, epsilon, rep)
    fname = fname.replace(".","_") + ".txt"
    print("Save to : %s" % (fname))
    with open(fname,"w") as f:
        for [phi,p,noanswer] in zip(phi_arr,power_arr,noanswer_arr):
            f.write("%f,%f,%f\n" % (phi,p,noanswer))
    f.close()

def run_test(phi0, m, delta, epsilon0, epsilon ,repetitions):


    pi0 = range(1, m + 1)
    power_arr = []
    phi_arr = []
    noanswer_arr = []
    test_fixed_confidence = SimpleFixedConfidence(pi0, phi0, delta, epsilon0, epsilon, debug=False)
    sampcomp = test_fixed_confidence.get_sample_num()
    print("Running: phi0_%g_m_%d_delta_%g_eps0_%g_eps_%g_rep_%d" % (phi0, m, delta, epsilon0, epsilon, repetitions))
    print("samp comp: %d" % (sampcomp))
    print("H_0: [%g,%g]" % (phi0-epsilon0,phi0+epsilon0))

    # right
    test_anymore = True
    step = 0.0005
    for phi in np.arange(phi0,1.0,step):
        threshold = (np.sqrt(m) / 4.0) * np.log( (phi- 3 * step) / (phi0 + epsilon0))
        if (test_anymore):
            if (test_anymore):
                if (phi <= phi0 + epsilon0 - step):
                    power = 0
                    noanswer = 0
                    print("-1> phi: %f\tpower: %f, noanswer: %g" % (phi, power, noanswer))
                elif ((phi >= phi0 + epsilon0 + 3 * step) and (threshold  < epsilon)):
                    power = 0
                    noanswer = 1
                    print("-2> phi: %f\tpower: %f, noanswer: %g" % (phi, power, noanswer))
                else:
                    #[power, noanswer] = get_power(test_fixed_confidence, model, repetitions)
                    [power, noanswer] = get_power_parallel(test_fixed_confidence, pi0, phi, repetitions)
                    print("phi: %f\tpower: %f, noanswer: %g" % (phi, power, noanswer))
        else:
            power = 1.0
            noanswer = 0.0

        phi_arr.append(phi)
        power_arr.append(power)
        noanswer_arr.append(noanswer)

        if ((power > 0.99) & (noanswer < 0.01)):
            test_anymore = False

        #save_power_curve(phi_arr, power_arr, noanswer_arr, phi0, m, delta, epsilon0, epsilon, repetitions)

    # left
    test_anymore = True
    for phi in np.arange(phi0,0.0,-step):
        threshold = (np.sqrt(m) / 4.0) * np.log((phi0 -epsilon0) / (phi-3*step))
        if (test_anymore):
            if (phi >= phi0 - epsilon0 + step):
                power = 0
                noanswer = 0
                print("-1> phi: %f\tpower: %f, noanswer: %g" % (phi, power, noanswer))
            elif ((phi <= phi0 - epsilon0 - 3 * step) and (threshold < epsilon)):
                power = 0
                noanswer = 1
                print("-2> phi: %f\tpower: %f, noanswer: %g" % (phi, power, noanswer))
            else:
                #[power, noanswer] = get_power_parallel(test_fixed_confidence, model, repetitions)
                [power, noanswer] = get_power_parallel(test_fixed_confidence, pi0, phi, repetitions)
                print("phi: %f\tpower: %f, noanswer: %g" % (phi, power, noanswer))
        else:
            power = 1.0
            noanswer = 0.0

        phi_arr.insert(0,phi)
        power_arr.insert(0,power)
        noanswer_arr.insert(0,noanswer)

        if ((power>0.99) & (noanswer<0.01)):
            test_anymore = False

        #save_power_curve(phi_arr, power_arr, noanswer_arr, phi0, m, delta, epsilon0, epsilon, repetitions)

    save_power_curve(phi_arr, power_arr, noanswer_arr, phi0, m, delta, epsilon0, epsilon, repetitions)



if __name__ == '__main__':
    m = 6
    phi0 = 0.5
    delta = 0.05
    repetitions = 20

    epsilon0 = 0.05
    epsilon = 0.01

    #run_test(pi0, phi0, m, delta, epsilon0, epsilon, repetitions)
    for m in [10]:
        for phi0 in [0.1, 0.5, 0.9]:
            for epsilon in [0, 0.01, 0.05]:
            #for epsilon in [0.05]:
                run_test(phi0, m, delta, epsilon0, epsilon, repetitions)
    # starttime = time.time()
    # processes = []
    # for m in [5,10,20,30,50,150]:
    #     for epsilon in [0, 0.01, 0.05, 0.1]:
    #         p = multiprocessing.Process(target=run_test, args=(phi0, m, delta, epsilon0, epsilon, repetitions))
    #         processes.append(p)
    #         p.start()
    #
    # for process in processes:
    #     process.join()
    #
    # print('That took {} seconds'.format(time.time() - starttime))
