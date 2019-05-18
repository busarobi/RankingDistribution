import sys
sys.path.append('./trank/')

from trank import Mallows
import numpy as np
from trank.test_simple import SimpleFixedConfidence
import time
import multiprocessing



def worker(procnum, return_dict, m, phi, n):
    avg_rankings = np.zeros((m,))
    pi0 = range(1, m + 1)
    model = Mallows(pi0, phi)
    for i in range(n):
        ranking = model.get_sample()
        for i, r in enumerate(ranking):
            avg_rankings[i] += r

    est_rank = np.argsort(avg_rankings)

    #print str(procnum) + ' represent!'
    if (np.array_equal(est_rank, range(m))):
        return_dict[procnum] = 1
    else:
        return_dict[procnum] = 0


def get_power(n, m, phi, repetitions):
    return_dict = dict()

    np.zeros((repetitions,))
    for i in range(repetitions):
        worker(i, return_dict, m, phi, n)

    return np.average(return_dict.values())


def get_power_parallel(n, m, phi, repetitions):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(repetitions):
        p = multiprocessing.Process(target=worker, args=(i, return_dict, m, phi, n))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    return np.average(return_dict.values())



def run_test_central(phi0, m, delta, repetitions):

    acc_arr = []
    sampnum = 1/0.01 * np.log(m/delta)
    with (open("./results/central_rank_results_2.txt", "a")) as f:
        for n in sampnum:
            if ((len(acc_arr)>=1) and (acc_arr[len(acc_arr)-1]==1.0)):
                acc = 1.0
            else:
                acc = get_power(n, m, phi0, repetitions)

            acc_arr.append(acc)
            print( "m:% g\tphi: %g, sample_size: %g, acc: %g" % (m, phi0, n, acc))

        s = "m:%g,phi:%g" % (m, phi0)
        for n, acc in zip(eval_arr,acc_arr):
            s += (",%d:%g" % (n,acc))
        s += "\n"
        print(s)
        f.write(s)
        f.flush()
    f.close()


if __name__ == '__main__':
    m = 6
    phi0 = 0.5
    delta = 0.05
    repetitions = 100

    epsilon0 = 0.05
    epsilon = 0.01

    fname = "./results/avg_rank_results_2.txt"
    with (open(fname, "w")) as f:
        f.write("")
    f.close()

    #run_test(pi0, phi0, m, delta, epsilon0, epsilon, repetitions)
    #for phi0 in [0.1, 0.3, 0.5, 0.7, 0.9]:
    for phi0 in [0.1, 0.5, 0.9]:
        #for m in [5,10,20,30,50,150]:
        for m in [5, 10, 50]:
                run_test_central(phi0, m, repetitions)
