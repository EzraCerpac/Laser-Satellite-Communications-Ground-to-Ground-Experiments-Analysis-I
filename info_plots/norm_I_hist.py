import numpy as np
from matplotlib import pyplot as plt

from formula.normalize import norm_I


def norm_I_hist(I, density: bool = True, bins: int = 12, plot=True) -> np.ndarray:
    if plot:
        return plt.hist(norm_I(I, False), bins=bins, density=density, label='normalized irradiance')[0]
    else:
        return np.histogram(norm_I(I, False), bins=bins, density=density)[0]
