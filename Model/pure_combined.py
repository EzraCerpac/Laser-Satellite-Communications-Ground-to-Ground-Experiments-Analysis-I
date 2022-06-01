from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import quad
from scipy.optimize import curve_fit
from scipy.stats import lognorm, beta

from formula.statistics import cost
from plotting.norm_I_hist import norm_I_hist


# @lru_cache(maxsize=None)
def func(X, beta_b, log_a, log_b):
    # return beta.pdf(X, beta_b, 1) * lognorm.pdf(X, log_a, log_b)
    return [quad(lambda I0: beta.pdf(I0, beta_b, 1) * lognorm.pdf(x, log_a, log_b), 0, 1)[0] for x in X]


def combined_curve_fit(irradiance: np.ndarray, res: int = 101, plot: bool = True) -> Tuple[float, float, float, float]:
    yy = norm_I_hist(irradiance, bins=res, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    p_opt, p_cov = curve_fit(func, xx, yy, p0=[2.71, 0.0935, -0.4])
    if plot:
        plt.plot(xx, beta.pdf(xx, *p_opt), label='beta fitment')
    yy = norm_I_hist(irradiance, bins=250, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    return *p_opt, cost(func, xx, yy, p_opt)
