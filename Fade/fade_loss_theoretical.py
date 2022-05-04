import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
from scipy import special
import combined_fit.indices


def PDF_gamma(Ft): #gamma-gamma
    Lambda = 1550e-9
    # Cn_2 = 3.69125616594868e-14
    L = 10000
    D = 3.45
    P0 = 1000
    Cn_data = pd.read_pickle('Data/DFs/Cn.pickle')
    k = 2 * np.pi / Lambda
    # sigma_R = np.sqrt(1.23 * Cn_2 * k ** (7 / 6) * L ** (11 / 6))
    sigma_R = combined_fit.indices.rytov_index(k, np.array(Cn_data['Cn^2']), np.array(Cn_data['z-distance']))
    alpha = (np.exp(0.49*(sigma_R**2)/(1+1.11*(sigma_R**(12/5)))**(7/6))-1)**(-1)
    beta = (np.exp(0.51*(sigma_R**2)/(1+0.69*(sigma_R**(12/5)))**(5/6))-1)**(-1)
    T_alpha = special.gamma(alpha)
    T_beta = special.gamma(beta)
    I = 1.0
    #gamma = np.empty(0)

    gamma = (2*(alpha * beta)**((alpha+beta)/2) / (T_alpha*T_beta*I)) * ((np.exp(-0.23*Ft))**((alpha+beta)/2)) * special.kv(
                alpha - beta, 2 * np.sqrt(alpha * beta * np.exp(-0.23*Ft)))
    print(sigma_R)
    return gamma

def PDF_gamma_test():
    prob = []
    ft = []

    for i in range(11):
       ft.append(i)
       prob.append(PDF_gamma(i))

    print(prob)
    print(ft)

    plt.plot(ft, prob)
    plt.show()



