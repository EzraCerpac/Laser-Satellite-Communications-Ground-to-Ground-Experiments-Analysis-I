import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import beta

from combined_fit.bridge import residu_angular_jitter
from formula.jitter import calc_sigma
from formula.normalize import norm_I


def beta_func(I: np.ndarray, beta: float, scale: float) -> float:
    return beta * (I / scale) ** (beta - 1)


def calc_beta(I: np.ndarray) -> float:
    I_n = (norm_I(I) + 1e-10) / (1 + 1e-8)
    return beta.fit(I_n, fa=1, floc=0, fscale=1)[1]


def fit_beta_to_hist(freqs: np.ndarray, ii: np.ndarray) -> tuple[float, np.float]:
    p_opt, _ = curve_fit(beta_func, ii, freqs, (3., 2.))
    return p_opt[0], p_opt[1]  # code for norm_residu: freqs * p_opt[1] ** (p_opt[0] - 1)


def plot_angular_jitter_dist(bet: float, scale: float = 1, ii: np.ndarray = np.linspace(0, 1, 101)) -> None:
    plt.plot(ii, beta_func(ii, bet, scale), label='angular jitter dist')


def estimate_sigma(I: np.ndarray, w_0: float, res: int = 1001, usable: float = 0.2, plot: bool = False) -> float:
    usable_indices = int(res * usable)
    ii = np.linspace(0, 1, res)
    residu = residu_angular_jitter(I, res, plot)[:usable_indices]
    beta, scale = fit_beta_to_hist(residu, ii[:usable_indices])
    if plot:
        plot_angular_jitter_dist(beta, scale)
    sigma = calc_sigma(beta, w_0)
    return sigma
