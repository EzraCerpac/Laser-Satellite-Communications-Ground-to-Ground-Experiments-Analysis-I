import numpy as np
from numba import jit

@jit(nopython=True, parallel=True)
def norm_I(I: np.ndarray) -> np.ndarray:
    # TODO: incorperate I = np.percentile(I, [0, 100])
    imin, imax = min(I), max(I)
    I_N = (I - imin) / (imax - imin)
    return I_N
