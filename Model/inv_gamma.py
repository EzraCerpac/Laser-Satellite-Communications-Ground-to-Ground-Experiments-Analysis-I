from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import invgamma

from formula.normalize import norm_I


def inv_gamma(irradiance: np.ndarray, plot: bool = True) -> Tuple[float, float]:
    I = norm_I(irradiance)
    p = invgamma.fit(I, fscale=1)
    if plot:
        xx = np.linspace(1e-8, 1 - 1e-8, 101)
        plt.plot(xx, invgamma.pdf(xx, *p), label='inverse gamma fitment')
    return p[0], p[1]
