import numpy as np
import matplotlib.pyplot as plt

def Ap_Av(k, D, L):
    return (1 + 1.062 * ((k * D ** 2) / (4 * L))) ** (7/6)

def Sigma_I(Sigma_R):
    return np.exp((0.49 * Sigma_R ** 2)/(1 + 1.11 * Sigma_R ** (12/5)) + (0.51 * Sigma_R ** 2)/(1 + 0.69 * Sigma_R ** (12/5)) ** (5 / 6)) - 1

def Sigma_R(Cn, k, L):
    return 1.23 * Cn ** 2 * k ** (7/6) * L ** (11 / 6)

def Sigma_P(A, Sigma_I):
    return A * Sigma_I ** 2

def p_P(P_RX, Sigma_P, P0):
    a = 1 / (P_RX * (2 * np.pi * np.log(Sigma_P ** 2 +1)) ** (1/2))
    b = - (np.log(P_RX / P0) + 0.5 * np.log(Sigma_P ** 2 +1)) ** 2 / (2 * np.log(Sigma_P ** 2 + 1))
    return a * np.exp(b)

#k is 2*pi/lambda, D is reciever diameter

Lambda = 1550e-9
Cn = 0.033
L = 10000
D = 3.45
P0 = 100000
k = 2 * np.pi / Lambda

A = Ap_Av(k, D, L)
SigR = Sigma_R(Cn, k , L)
SigI = Sigma_I(SigR)
SigP = Sigma_P(A, SigI)

PRl = np.linspace(0,101)
pPl = p_P(PRl, SigP, P0)

plt.plot(PRl,pPl)
plt.show()

