import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import math
from combined_fit.indices import rytov_index
from formula.jitter import k
import pandas as pd

linestyles = ['o-', 'D-', '^-', 's-', '*-', 'P-']

wavelambda = 1550e-9
Cn = pd.read_pickle('Data/DFs/Cn.pickle') if __name__ != '__main__' else pd.read_pickle('../Data/DFs/Cn.pickle')

def Sigma_R2():
    Sigma_R2 = (rytov_index(k(wavelambda), np.array(Cn['z-distance']), np.array(Cn['Cn^2'])))

    return Sigma_R2

def Sigma_I2(Sigma_R2):
    """

    :param Sigma_R2: Rytov Index
    :return: Intensity Scintillation Index
    """
    Sigma_I2 = np.exp((0.49 * Sigma_R2) / (1 + 1.11 * Sigma_R2 ** (6 / 5)) + (0.51 * Sigma_R2) / (
            1 + 0.69 * Sigma_R2 ** (6 / 5)) ** (5 / 6)) - 1
    return Sigma_I2

def frac_fade_time(Ft):
    r2 = 0
    W_LT2 = 1
    sigma_I = np.sqrt(Sigma_I2(Sigma_R2()))
    P_fade_time = 0.5 * (1 + math.erf(0.5*Sigma_I2(Sigma_R2()) + 2*r2/W_LT2 - 0.23*Ft / (math.sqrt(2)*sigma_I)))
    return P_fade_time

def frac_fade_time_test():
    prob = []
    Ft = []

    for i in range(11):
       Ft.append(i)
       prob.append(frac_fade_time(i))

    plt.plot(Ft, prob, linestyles.pop(),label='lognormal model')

def frac_fade_time_irradiance():
    prob = []
    I_T = []

    for i in range(11):
       I_T.append(1/(10**(i/10)))
       prob.append(frac_fade_time(i))

    print(prob)
    print(I_T)

    plt.plot(I_T, prob)
    plt.ylabel(r'Probability of Fade')
    plt.xlabel(r'Irradiance Level $I_T$ (W/$m^2$)')
    plt.tight_layout()
    plt.show()


