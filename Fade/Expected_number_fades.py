import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import special, interpolate, integrate
import combined_fit.indices
from formula.jitter import k


wavelambda = 1550e-9
Cn = pd.read_pickle('Data/DFs/Cn.pickle') if __name__ != '__main__' else pd.read_pickle('../Data/DFs/Cn.pickle')
Lambda = 1550e-9
Cn_data = pd.read_pickle('Data/DFs/Cn.pickle')
sigma_R = combined_fit.indices.rytov_index(k(Lambda), np.array(Cn_data['z-distance']), np.array(Cn_data['Cn^2']))
alpha = (np.exp(0.49 * (sigma_R ** 2) / (1 + 1.11 * (sigma_R ** (12 / 5))) ** (7 / 6)) - 1) ** (-1)
beta = (np.exp(0.51 * (sigma_R ** 2) / (1 + 0.69 * (sigma_R ** (12 / 5))) ** (5 / 6)) - 1) ** (-1)
T_alpha = special.gamma(alpha)
T_beta = special.gamma(beta)
Sigma_R2 = sigma_R**2

def Sigma_I2(Sigma_R2):
    Sigma_R2 = (combined_fit.indices.rytov_index(k(Lambda), np.array(Cn_data['z-distance']), np.array(Cn_data['Cn^2'])))**2
    Sigma_I2 = np.exp((0.49 * Sigma_R2) / (1 + 1.11 * Sigma_R2 ** (6 / 5)) + (0.51 * Sigma_R2) / (
            1 + 0.69 * Sigma_R2 ** (6 / 5)) ** (5 / 6)) - 1
    return Sigma_I2

# expected number of fades log-normal
def v_0():
    h = 900
    l_0 = 1
    L_0 = 4/(1+((h-8500) / 2500))
    k = 1
    k_0 = 2*np.pi / (L_0 * l_0)
    k_m = 5.92 / l_0
    C_n2 = 1
    v_0 = 1/(2*np.pi) * (((0.033 * C_n2 * np.exp(-k**2 / k_m**2) )/ (k**2 + k_0**2)**(11/6))**0.5)
    return v_0

def enf_log(F_T,v_0): #expected number of fade log-normal
    r = 0
    W_LT2 = 1
    enf_log = v_0 * np.exp(-(0.5* Sigma_I2(Sigma_R2)+2*r/W_LT2 - 0.23*F_T)**2 / 2* Sigma_I2(Sigma_R2))
    return enf_log

def enf_gam(F_T,v_0):# expected number gamma-gamma
    Sigma_I = np.sqrt(Sigma_I2(Sigma_R2))
    enf_gam = (2*(2**0.5)*np.pi*alpha*beta* v_0 * Sigma_I)/(T_alpha * T_beta)*(alpha*beta*np.exp(-0.23*F_T))**(alpha+beta-1/ 2) * special.kv(
        alpha - beta,2 * np.sqrt(alpha * beta * np.exp(-0.23 * F_T)))
    return enf_gam

def enf_gam_TEST():
    prob = []
    Ft = []

    for i in range(11):
       Ft.append(i)
       prob.append(enf_gam(i,v_0()))

    plt.plot(Ft, prob)
    plt.yscale('log')
    plt.show()

def enf_log_TEST():
    prob = []
    Ft = []

    for i in range(11):
       Ft.append(i)
       prob.append(enf_log(i,v_0()))

    plt.plot(Ft, prob)
    plt.yscale('log')
    plt.show()
