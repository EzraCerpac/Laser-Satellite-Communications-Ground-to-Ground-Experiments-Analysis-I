from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import invgamma

from formula.normalize import norm_I
from formula.statistics import cost
from plotting.norm_I_hist import norm_I_hist


def inv_gamma_curve_fit(irradiance: np.ndarray, res: int = 101, plot: bool = True) -> Tuple[float, float]:
    yy = norm_I_hist(irradiance, bins=res, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    p_opt, p_cov = curve_fit(invgamma.pdf, xx, yy,
                             p0=[3, -0.001])  # TODO: check if fscale=1 is correct
    if plot:
        plt.plot(xx, invgamma.pdf(xx, *p_opt), label='inverse gamma fitment')
    yy = norm_I_hist(irradiance, bins=250, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    return *p_opt, cost(invgamma.pdf, xx, yy, p_opt)


def inv_gamma(irradiance: np.ndarray, plot: bool = True) -> Tuple[float, float, float]:
    I = norm_I(irradiance)
    p = invgamma.fit(I, fscale=1)
    xx = np.linspace(1e-8, 1 - 1e-8, 101)
    if plot:
        plt.plot(xx, invgamma.pdf(xx, *p), label='inverse gamma fitment')
    yy = norm_I_hist(irradiance, bins=250, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    return p[0], p[1], cost(invgamma.pdf, xx, np.histogram(I, bins=len(xx), density=True)[0], p)
