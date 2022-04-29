from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import invgamma

from plotting.norm_I_hist import norm_I_hist


def inv_gamma(irradiance: np.ndarray, res: int = 1001, plot: bool = True) -> Tuple[float, float]:
    yy = norm_I_hist(irradiance, bins=res, plot=False)
    xx = np.linspace(1e-10, 1, len(yy))
    p_opt, p_cov = curve_fit(invgamma.pdf, xx, yy,
                             p0=[3, -0.001])  # TODO: check if fscale=1 is correct
    if plot:
        plt.plot(xx, invgamma.pdf(xx, *p_opt), label='inverse gamma fitment')
    return *p_opt, np.sqrt(p_cov[0, 0])
