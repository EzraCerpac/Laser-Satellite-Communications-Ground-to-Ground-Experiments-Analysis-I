from functools import partial
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from scipy.special import gamma, kv

from formula.normalize import norm_I
from formula.statistics import cost
from plotting.norm_I_hist import norm_I_hist


def gamma_gamma_paper(irradiance: np.ndarray, sigma_r2: float, irradiance_avg: float = None) -> np.ndarray:
    if irradiance_avg is None: irradiance_avg = np.mean(irradiance)
    alpha = (np.exp((0.49 * sigma_r2) / ((1 + 1.11 * sigma_r2 ** (6 / 5)) ** (7 / 6))) - 1) ** -1
    beta = (np.exp((0.51 * sigma_r2) / ((1 + 0.69 * sigma_r2 ** (6 / 5)) ** (5 / 6))) - 1) ** -1
    return (2 * (alpha * beta) ** ((alpha + beta) / 2)) / (gamma(alpha) * gamma(beta) * irradiance) * (
                (irradiance / irradiance_avg) ** ((alpha + beta) / 2)) * kv(alpha - beta, 2 * np.sqrt(
        (alpha * beta * irradiance) / irradiance_avg))


def gamma_gamma_paper_curve_fit(irradiance: np.ndarray, res: int = 101, plot: bool = True) -> Tuple[float, float]:
    yy = norm_I_hist(irradiance, bins=res, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    I0 = np.mean(norm_I(irradiance))
    func = partial(gamma_gamma_paper, irradiance_avg=I0)
    p_opt, p_cov = curve_fit(func, xx, yy, p0=[0.1])
    if plot:
        plt.plot(xx, func(xx, *p_opt), label='gamma gamma fitment')
    yy = norm_I_hist(irradiance, bins=250, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    return *p_opt, I0, cost(func, xx, yy, p_opt)