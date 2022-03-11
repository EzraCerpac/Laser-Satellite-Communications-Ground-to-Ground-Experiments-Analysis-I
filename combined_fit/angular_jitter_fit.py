import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import beta

from formula.normalize import norm_I


def calc_beta(I: np.ndarray) -> float:
    I_n = (norm_I(I) + 1e-10) / (1 + 1e-8)
    return beta.fit(I_n, fa=1, floc=0, fscale=1)[1]


def calc_sigma(beta: float, w_0: float) -> float:
    sigma = np.sqrt(w_0 ** 2 / beta)
    return sigma


def plot_angular_jitter_dist(I: np.ndarray, bet: float, ii: np.ndarray = np.linspace(0, 1, 101)):
    plt.hist(norm_I(I), bins=101, density=True, label='normalized irradiance')
    plt.plot(ii, beta.pdf(ii, 1, bet), 'r-', label='angular jitter dist')
    # plt.ylim(0, 10)
    plt.legend()
