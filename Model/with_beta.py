import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.integrate import quad
from scipy.optimize import curve_fit
from scipy.stats import beta as beta_func
from functools import partial

from combined_fit.angular_jitter_fit_gamma import gamma_gamma, alphafun, betafun
from combined_fit.indices import scintillation_index, rytov_index_const
from combined_fit.scintillation import probability_dist
from formula.jitter import k, calc_sigma
from formula.statistics import MSE
from plotting.norm_I_hist import norm_I_hist


Cn = pd.read_pickle('Data/DFs/Cn.pickle')
zz = np.array(Cn['z-distance'])
C_n2 = np.array(Cn['Cn^2'])

labda = 1550e-9


def estimate_sigma(irradiance: np.ndarray, w_0: float, use_gamma: bool = False, res: int = 100, plot=False,
                   full_fit: bool = False):
    scint_func = combined_dist_gamma if use_gamma else combined_dist
    yy = norm_I_hist(irradiance, bins=res, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    if full_fit and use_gamma is False:
        (alpha, beta, sigma_i), p_cov = curve_fit(partial(scint_func, full_fit=full_fit), xx, yy, p0=[2, 5, 0.2],
                                                  bounds=((0.5, 0.5, 0), (20, 20, 10)))
    elif full_fit and use_gamma is True:
        (alpha, beta, a, b), p_cov = curve_fit(partial(scint_func, full_fit=full_fit), xx, yy, p0=[2, 5, 2, 8],
                                               bounds=((0.5, 0.5, 0, 0), (20, 20, 20, 20)))
    else:
        (alpha, beta), p_cov = curve_fit(partial(scint_func, full_fit=full_fit), xx, yy, p0=[2, 5], bounds=((0.5, 0.5), (20, 20)))
    if plot:
        xx_for_plot = np.linspace(1e-10, 1, 1001)
        label = 'gamma fitment' if use_gamma else 'lognormal fitment'
        if full_fit and use_gamma is False:
            plt.plot(xx_for_plot, scint_func(xx_for_plot, alpha, beta, sigma_i, full_fit=full_fit), label=label)
        elif full_fit and use_gamma is True:
            plt.plot(xx_for_plot, scint_func(xx_for_plot, alpha, beta, a, b, full_fit=full_fit), label=label)
        else:
            plt.plot(xx_for_plot, scint_func(xx_for_plot, alpha, beta, full_fit=full_fit), label=label)

    if not full_fit:
        return calc_sigma(beta, w_0), alpha, beta, MSE(scint_func, xx, yy, (alpha, beta))
    elif full_fit and use_gamma:
        return calc_sigma(beta, w_0), alpha, beta, a, b, MSE(scint_func, xx, yy, (alpha, beta, a, b, True))
    else:
        return calc_sigma(beta, w_0), alpha, beta, sigma_i, MSE(scint_func, xx, yy, (alpha, beta, sigma_i, True))


def combined_dist(X: np.ndarray, alpha: float, beta: float, sigma_i: float = 0, full_fit: bool = False):
    """Lognormal implementation"""

    if not full_fit:
        sigma_i = scintillation_index(rytov_index_const(k(labda), zz[-1], C_n2.mean()))

    return [quad(lambda I: beta_func.pdf(I, alpha, beta) * probability_dist(
        i, I, sigma_i), 0, 1)[0] for i in X]


def combined_dist_gamma(X: np.ndarray, alpha: float, beta: float, a: float = 0, b: float = 0, full_fit: bool = False):
    if not full_fit:
        a = alphafun()
        b = betafun()

    return [quad(lambda I: beta_func.pdf(I, alpha, beta) * gamma_gamma(i, I, a, b), 0, 1)[0] for i in X]


def random_dist_test(X: list, beta: float, alfa: float, sigma: float):
    return [quad(lambda a: beta * i ** 3 * a ** 2 + alfa * i ** 2 * np.log(a) - sigma * 10 * i + beta, 0, 1)[0] for i in
            X]
