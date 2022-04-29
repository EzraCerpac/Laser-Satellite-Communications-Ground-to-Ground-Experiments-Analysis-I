from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import lognorm

from plotting.norm_I_hist import norm_I_hist


def lognormal(irradiance: np.ndarray, res: int = 1001, plot: bool = True) -> Tuple[float, float]:
    yy = norm_I_hist(irradiance, bins=res, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    p_opt, p_cov = curve_fit(lognorm.pdf, xx, yy, p0=[1, -0.0001])
    if plot:
        plt.plot(xx, lognorm.pdf(xx, *p_opt), label='lognormal fitment')
    return *p_opt, np.sqrt(p_cov[0, 0])
