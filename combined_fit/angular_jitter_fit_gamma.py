import math
from scipy import special
from combined_fit.I_0_calc import main
from combined_fit.indices import rytov_index
from formula.jitter import k
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from formula.normalize import norm_I

wavelambda = 1550 * 10 ** -9
Cn = pd.read_pickle('../Data/DFs/Cn.pickle')
def alphafun(Rytov=math.sqrt(rytov_index(k(wavelambda), np.array(Cn['z-distance']), np.array(Cn['Cn^2'])))):
    return math.e ** (0.49 * Rytov ** 2 / (1 + 1.11 * Rytov ** (12 / 5)) ** (7 / 6)) - 1


def betafun(Rytov=math.sqrt(rytov_index(k(wavelambda), np.array(Cn['z-distance']), np.array(Cn['Cn^2'])))):
    return math.e ** (0.51 * Rytov ** 2/ (1 + 0.69 * Rytov ** (12 / 5)) ** (5 / 6)) - 1

def gamma_gamma(I: np.ndarray, alpha=alphafun(), beta=betafun(),mai=main()):
    gamma = np.empty(0)
    for i in range(I.shape[0]):
        gamma = np.append(gamma,((2 * (alpha * beta) ** ((alpha + beta) / 2 - 1)) / (special.gamma(alpha) * special.gamma(beta) * I[i])) * ((I[i]) ** ((alpha + beta) / 2)) * special.kv(alpha - beta, 2 * math.sqrt(alpha * beta * I[i])))
    return(gamma)

if __name__ == '__main__':
   I = np.array(pd.read_pickle('../Data/DFs/data18/off1.pickle'))
   gamma_pdf = gamma_gamma(norm_I(I, True))
   print(gamma_pdf)
   plt.plot(norm_I(I, True),gamma_pdf)
   plt.show()

