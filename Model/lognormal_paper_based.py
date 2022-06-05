from functools import partial
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from formula.normalize import norm_I
from formula.statistics import cost
from plotting.norm_I_hist import norm_I_hist


def lognormal_paper(irradiance: np.ndarray, sigma_i2: float, mu: float, irradiance_avg: float = None) -> np.ndarray:
    if irradiance_avg is None: irradiance_avg = np.mean(irradiance)

    return (1 / (irradiance * np.sqrt(sigma_i2 * 2 * np.pi))) * np.exp(
        -((np.log(irradiance / irradiance_avg) - mu) ** 2 / (2 * sigma_i2)))


def lognormal_paper_true(irradiance: np.ndarray, sigma_i2: float, irradiance_avg: float = None) -> np.ndarray:
    irradiance = irradiance
    if irradiance_avg is None: irradiance_avg = np.mean(irradiance)
    return (1 / (irradiance * np.sqrt(2 * np.pi * sigma_i2))) * np.exp(
        -((np.log(irradiance / irradiance_avg) + 0.5 * sigma_i2) ** 2 / (2 * sigma_i2)))


def lognormal_paper_curve_fit(irradiance: np.ndarray, res: int = 101, plot: bool = True) -> Tuple[float, float]:
    yy = norm_I_hist(irradiance, bins=res, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    I0 = 0.5
    func = partial(lognormal_paper, irradiance_avg=I0)
    p_opt, p_cov = curve_fit(func, xx, yy, p0=[0.05, -0.1])
    if plot:
        plt.plot(xx, func(xx, *p_opt), label='lognormal fitment')
    yy = norm_I_hist(irradiance, bins=250, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    return *p_opt, I0, cost(func, xx, yy, p_opt)


def lognormal_paper_true_curve_fit(irradiance: np.ndarray, res: int = 101, plot: bool = True) -> Tuple[float, float]:
    yy = norm_I_hist(irradiance, bins=res, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    I0 = np.mean(norm_I(irradiance))
    func = partial(lognormal_paper_true, irradiance_avg=I0)
    p_opt, p_cov = curve_fit(func, xx, yy, p0=[2.])
    if plot:
        plt.plot(xx, func(xx, *p_opt), label='lognormal fitment')
    yy = norm_I_hist(irradiance, bins=250, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    return *p_opt, I0, cost(func, xx, yy, p_opt)
