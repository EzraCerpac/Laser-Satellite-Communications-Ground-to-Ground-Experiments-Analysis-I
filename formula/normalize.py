import numpy as np


def norm_I(I: np.ndarray) -> np.ndarray:
    imin, imax = min(I), max(I)
    I_N = (I - imin) / (imax - imin)
    return I_N
