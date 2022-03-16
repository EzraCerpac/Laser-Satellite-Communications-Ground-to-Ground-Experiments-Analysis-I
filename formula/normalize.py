import numpy as np


def norm_I(I: np.ndarray) -> np.ndarray:
    # TODO: incorperate I = np.percentile(I, [0, 100])
    imin, imax = min(I), max(I)
    I_N = (I - imin) / (imax - imin)
    return I_N
