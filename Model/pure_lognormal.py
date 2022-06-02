from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import lognorm

from formula.normalize import norm_I
from formula.statistics import cost
from plotting.norm_I_hist import norm_I_hist


def lognormal(irradiance: np.ndarray, plot: bool = True) -> Tuple[float, float, float]:
    I = norm_I(irradiance)
    p = lognorm.fit(I, fscale=1)
    xx = np.linspace(1e-8, 1 - 1e-8, 101)
    if plot:
        plt.plot(xx, lognorm.pdf(xx, *p), label='lognormal fitment')
    yy = norm_I_hist(irradiance, bins=250, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    return p[0], p[1], cost(lognorm.pdf, xx, np.histogram(I, bins=len(xx), density=True)[0], p)


def lognormal_curve_fit(irradiance: np.ndarray, res: int = 101, plot: bool = True) -> Tuple[float, float]:
    yy = norm_I_hist(irradiance, bins=res, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    p_opt, p_cov = curve_fit(lognorm.pdf, xx, yy, p0=[1, -0.001])
    if plot:
        plt.plot(xx, lognorm.pdf(xx, *p_opt), label='lognormal fitment')
    yy = norm_I_hist(irradiance, bins=250, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    return *p_opt, cost(lognorm.pdf, xx, yy, p_opt)

# def lognormal_curve_fit_fixed(irradiance: np.ndarray, res: int = 101, plot: bool = True) -> Tuple[float, float]:
#     yy = norm_I_hist(irradiance, bins=res, plot=False)
#     xx = np.linspace(1e-10, 1, len(yy))
#     func = lambda x, sigma: lognorm.pdf(x, sigma, -sigma/2)
#     p_opt, p_cov = curve_fit(func, xx, yy, p0=[0.05**(1/2)])
#     if plot:
#         plt.plot(xx, lognorm.pdf(xx, *p_opt), label='lognormal fitment')
#     yy = norm_I_hist(irradiance, bins=250, plot=False)
#     xx = np.linspace(1e-10, 1, len(yy))
#     return p_opt[0], -p_opt[0]/2, cost(func, xx, yy, p_opt)
