import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import beta

from formula.normalize import norm_I


def beta_func(I: np.ndarray, beta: float, scale: float) -> float:
    return beta * (I / scale) ** (beta - 1)


def calc_beta(I: np.ndarray) -> float:
    I_n = (norm_I(I) + 1e-10) / (1 + 1e-8)
    return beta.fit(I_n, fa=1, floc=0, fscale=1)[1]


def fit_beta_to_hist(freqs: np.ndarray, ii: np.ndarray) -> tuple[float, np.ndarray]:
    p_opt, _ = curve_fit(beta_func, ii, freqs, (3., 2.))
    # print(p_opt)
    # plt.plot(ii, freqs, label='original')
    # plt.plot(ii, beta_func(ii, *p_opt), label='fitted')
    # plt.legend()
    # plt.show()
    return p_opt[0], freqs * p_opt[1] ** (p_opt[0] - 1)


def calc_sigma(beta: float, w_0: float) -> float:
    sigma = np.sqrt(w_0 ** 2 / beta)
    return sigma


def plot_angular_jitter_dist(freqs: np.ndarray, bet: float, ii: np.ndarray = np.linspace(0, 1, 101)) -> None:
    plt.plot(ii, freqs, label='normalized irradiance')
    plt.plot(ii, beta.pdf(ii, bet, 1), 'r-', label='angular jitter dist')
    plt.legend()
    plt.show()
