import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.integrate import quad
from scipy.optimize import curve_fit
from scipy.stats import beta as beta_func

from combined_fit.angular_jitter_fit_gamma import gamma_gamma
from combined_fit.indices import scintillation_index, rytov_index_const
from combined_fit.scintillation import probability_dist
from formula.jitter import k, calc_sigma
from plotting.norm_I_hist import norm_I_hist

Cn = pd.read_pickle('Data/DFs/Cn.pickle')
zz = np.array(Cn['z-distance'])
C_n2 = np.array(Cn['Cn^2'])

labda = 1550e-9


def estimate_sigma(irradiance: np.ndarray, w_0: float, use_gamma: bool = False, res: int = 100, plot=False):
    scint_func = combined_dist_gamma if use_gamma else combined_dist
    yy = norm_I_hist(irradiance, bins=res, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    (alpha, beta), p_cov = curve_fit(scint_func, xx, yy, p0=[2, 5], bounds=((0.5, 0.5), (20, 20)))
    if plot:
        xx = np.linspace(1e-15, 1, 1001)
        label = 'gamma fitment' if use_gamma else 'lognormal fitment'
        plt.plot(xx, scint_func(xx, alpha, beta), label=label)
    return calc_sigma(beta, w_0), alpha, beta, np.sqrt(p_cov[0, 0])


def combined_dist(X: np.ndarray, alpha: float, beta: float):
    """Lognormal implementation"""
    return [quad(lambda I: beta_func.pdf(I, alpha, beta) * probability_dist(
        i, I, scintillation_index(rytov_index_const(
            k(labda), zz[-1], C_n2.mean()
        ))), 0, 1)[0] for i in X]


def combined_dist_gamma(X: np.ndarray, alpha: float, beta: float):
    return [quad(lambda I: beta_func.pdf(I, alpha, beta) * gamma_gamma(i, I), 0, 1)[0] for i in X]


def random_dist_test(X: list, beta: float, alfa: float, sigma: float):
    return [quad(lambda a: beta * i ** 3 * a ** 2 + alfa * i ** 2 * np.log(a) - sigma * 10 * i + beta, 0, 1)[0] for i in
            X]
