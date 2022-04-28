from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import lognorm

from formula.normalize import norm_I


def lognormal(irradiance: np.ndarray, plot: bool = True) -> Tuple[float, float]:
    I = norm_I(irradiance)
    p = lognorm.fit(I, fscale=1)
    if plot:
        xx = np.linspace(1e-8, 1 - 1e-8, 101)
        plt.plot(xx, lognorm.pdf(xx, *p), label='lognormal fitment')
    return p[0], p[1]
