import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import special, interpolate, integrate
from Fade.fade_loss_theoretical2 import frac_fade_time_test, linestyles
import combined_fit.indices
from formula.jitter import k

Lambda = 1550e-9
# Cn_2 = 3.69125616594868e-14
L = 10000
D = 3.45
P0 = 1000
Cn_data = pd.read_pickle('Data/DFs/Cn.pickle')
# Cn_data = Cn_data.iloc[1:]
sigma_R = combined_fit.indices.rytov_index(k(Lambda), np.array(Cn_data['z-distance']), np.array(Cn_data['Cn^2']))
alpha = (np.exp(0.49 * (sigma_R ** 2) / (1 + 1.11 * (sigma_R ** (12 / 5))) ** (7 / 6)) - 1) ** (-1)
beta = (np.exp(0.51 * (sigma_R ** 2) / (1 + 0.69 * (sigma_R ** (12 / 5))) ** (5 / 6)) - 1) ** (-1)
T_alpha = special.gamma(alpha)
T_beta = special.gamma(beta)


def PDF_gamma(Ft):  # gamma-gamma
    # sigma_R = np.sqrt(1.23 * Cn_2 * k ** (7 / 6) * L ** (11 / 6))
    I = 1.0
    # gamma = np.empty(0)

    gamma = (2 * (alpha * beta) ** ((alpha + beta) / 2) / (T_alpha * T_beta * I)) * (
                (np.exp(-0.23 * Ft)) ** ((alpha + beta) / 2)) * special.kv(
        alpha - beta, 2 * np.sqrt(alpha * beta * np.exp(-0.23 * Ft)))
    print(sigma_R)
    return gamma

def PDF_gamma_I(Z):  # gamma-gamma
    # sigma_R = np.sqrt(1.23 * Cn_2 * k ** (7 / 6) * L ** (11 / 6))
    I = 1.0
    # gamma = np.empty(0)

    gamma = (2 * (alpha * beta) ** ((alpha + beta) / 2) / (T_alpha * T_beta * I)) * (
                (Z) ** ((alpha + beta) / 2)) * special.kv(
        alpha - beta, 2 * np.sqrt(alpha * beta * Z))
    print(sigma_R)
    return gamma

def PDF_gamma_test():
    prob = []
    ft = []
    Z = []
    probx = []

    for i in range(11):
        Z.append(np.exp(-0.23*i))
        probx.append(PDF_gamma_I(i))

    for i in range(101):
       ft.append(i/100)
       prob.append(PDF_gamma(i/10))

    Gamma_Func = interpolate.interp1d(ft, prob, kind='cubic', fill_value="extrapolate")
    def g(x):
        return Gamma_Func(x)

    int_prob = []
    for i in range(0, 101, 1):
        estimatef_2, errorf = integrate.quad(g, ft[i], 1.1)
        int_prob.append(estimatef_2)

    ft_2 = []
    for i in range(101):
        ft_2.append(ft[i] * 10)

    #plt.plot(ft, prob)
    return ft_2, int_prob


def fade_loss():
    ft_2, int_prob = PDF_gamma_test()
    plt.plot(ft_2, int_prob, linestyles.pop(), markevery=10,label='gamma-gamma model')
    frac_fade_time_test()
    plt.legend()
    plt.ylabel('Probability of Fade')
    plt.xlabel('Threshold Level $F_T$ (dB)')
    plt.yscale('log')
    plt.savefig('Prob_of_Fade', format='pdf')
    plt.show()



