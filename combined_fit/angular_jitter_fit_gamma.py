from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import special

from combined_fit.indices import rytov_index
from formula.jitter import k
from formula.normalize import norm_I

wavelambda = 1550e-9
Cn = pd.read_pickle('Data/DFs/Cn.pickle') if __name__ != '__main__' else pd.read_pickle('../Data/DFs/Cn.pickle')


@lru_cache(maxsize=None)
def alphafun(Rytov=np.sqrt(rytov_index(k(wavelambda), np.array(Cn['z-distance']), np.array(Cn['Cn^2'])))):
    return (np.e ** (0.49 * Rytov ** 2 / (1 + 1.11 * Rytov ** (12 / 5)) ** (7 / 6)) - 1) ** - 1


@lru_cache(maxsize=None)
def betafun(Rytov=np.sqrt(rytov_index(k(wavelambda), np.array(Cn['z-distance']), np.array(Cn['Cn^2'])))):
    return (np.e ** (0.51 * Rytov ** 2 / (1 + 0.69 * Rytov ** (12 / 5)) ** (5 / 6)) - 1) ** - 1


def gamma_gamma(I: np.ndarray | float, I_0: float, alpha: float = alphafun(), beta: float = betafun()):
    # alpha, beta = alphafun(), betafun()
    gamma = np.empty(0)
    # print(I.shape[0])
    try:
        for i in range(I.shape[0]):
            gamma = np.append(gamma, ((2 * (alpha * beta) ** ((alpha + beta) / 2)) / (
                    special.gamma(alpha) * special.gamma(beta) * I[i])) * (
                                      (I[i] / I_0) ** ((alpha + beta) / 2)) * special.kv(
                alpha - beta, 2 * np.sqrt(alpha * beta * I[i] / I_0)))
    except IndexError:
        gamma = ((2 * (alpha * beta) ** ((alpha + beta) / 2)) / (
                special.gamma(alpha) * special.gamma(beta) * I)) * ((I / I_0) ** ((alpha + beta) / 2)) * special.kv(
            alpha - beta, 2 * np.sqrt(alpha * beta * I / I_0))
    return gamma


if __name__ == '__main__':
    I = np.array(pd.read_pickle('../Data/DFs/data18/off1.pickle'))
    I = norm_I(I)
    gamma_pdf = gamma_gamma(I, I.mean())
    print(gamma_pdf)
    plt.plot(I, gamma_pdf)
    plt.hist(I, density=True, bins='auto')
    plt.title('Gamma-gamma distribution with calculated alpha and beta')
    plt.xlabel(r'$I_{norm}$')
    plt.ylabel(r'$p(I)$')
    # plt.ylim(0,10)
    # plt.xlim((0,0.05))
    plt.show()
