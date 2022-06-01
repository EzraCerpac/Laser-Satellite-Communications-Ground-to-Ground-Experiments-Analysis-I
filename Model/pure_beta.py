from functools import partial
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import beta

from formula.normalize import norm_I
from formula.statistics import cost
from plotting.norm_I_hist import norm_I_hist


def beta_fit(irradiance: np.ndarray, plot: bool = True) -> Tuple[float, float, float]:
    I = norm_I(irradiance)
    p = beta.fit(I, fscale=1, fb=1)
    xx = np.linspace(1e-8, 1 - 1e-8, 101)
    if plot:
        plt.plot(xx, beta.pdf(xx, *p), label='beta fitment')
    yy = norm_I_hist(irradiance, bins=250, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    return p[0], p[1], cost(beta.pdf, xx, np.histogram(I, bins=len(xx), density=True)[0], p)


def beta_curve_fit(irradiance: np.ndarray, res: int = 101, plot: bool = True) -> Tuple[float, float, float]:
    yy = norm_I_hist(irradiance, bins=res, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    func = partial(beta.pdf, b=1)
    p_opt, p_cov = curve_fit(func, xx, yy, p0=[16])
    if plot:
        plt.plot(xx, beta.pdf(xx, *p_opt), label='beta fitment')
    yy = norm_I_hist(irradiance, bins=250, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    return *p_opt, 1, cost(func, xx, yy, p_opt)
