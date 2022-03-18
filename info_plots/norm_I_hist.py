import numpy as np
from matplotlib import pyplot as plt

from formula.normalize import norm_I


def norm_I_hist(I, density: bool = True, bins: int = 12) -> np.ndarray:
    return plt.hist(norm_I(I, True), bins=bins, density=density, label='normalized irradiance')[0]
