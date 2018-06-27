import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare

def get_basis_uniform(M):
    mat = np.zeros((M,M))
    fM = float(M)
    for i1 in range(M-1):
        for i2 in range(M):
            mat[i1,i2] = np.sqrt(2.0/fM)*np.cos(((i1+1)*np.pi*(i2+0.5))/fM)
    mat[M-1,:] = 1/fM

    return mat


def getf(p0, p_emp):
    fhat = (p_emp-p0) / np.sqrt(p0)
    return fhat

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

def Neyman_smooth_test_foruniform(obs):
    num_of_obs = np.sum(obs)
    p_emp = obs / num_of_obs
    order = len(obs)

    p0 = np.zeros((order,))
    p0[:] = 1 / float(order)

    basis = get_basis_uniform(order)
    fhat = getf(p0, p_emp)
    bs = getb(fhat, basis)

    #chisquares = np.zeros((order-1,))
    Mhat = np.zeros((order-1,))
    #chisquares[0] = num_of_obs * bs[0] * bs[0]
    Mhat[0] = (num_of_obs+1.0) / (num_of_obs-1.0) * bs[0] * bs[0] - 2.0 / (num_of_obs - 1.0) * getvjj( 0, p_emp, p0, basis)
    for i1 in range(1,order-1):
        #chisquares[i1] = chisquares[i1-1] + num_of_obs * bs[i1] * bs[i1]
        Mhat[i1] = Mhat[i1-1] + (num_of_obs+1.0) / (num_of_obs-1.0) * bs[i1] * bs[i1] - 2.0 / (num_of_obs - 1.0) * getvjj( i1, p_emp, p0, basis)



M=5
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

p_emp = np.zeros((M,))
p_emp[:] = 1/float(M)
p_emp[0] -= 1/(8.*float(M))
p_emp[M-1] += 1/(8.*float(M))

p_emp = p_emp / np.sum(p_emp)
print( "empricial")
print(p_emp)

fhat = getf(p0, p_emp)
print(fhat)
bs = getb(fhat,m)
print( "Fourier coeffs")
print(bs)
# for idx in range(M):
#     lab = "$%d$" % (idx+1)
#     plt.plot(range(1,M+1),m[idx,:], label=lab)
#
#
# plt.grid(True)
# plt.legend()
# plt.show()


chisquare([16, 18, 16, 14, 12, 12], f_exp=[16, 16, 16, 16, 16, 8])