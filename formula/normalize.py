import numpy as np
from scipy import stats
import logging


def norm_I(I: np.ndarray, remove_outlier: bool = False) -> np.ndarray:
    # logging.info(f" I: {np.size(I)}")
    if remove_outlier:
        I = stats.trimboth(I, 0.05)
    imin, imax = min(I), max(I)
    I_N = (I - imin) / (imax - imin)
    return I_N
