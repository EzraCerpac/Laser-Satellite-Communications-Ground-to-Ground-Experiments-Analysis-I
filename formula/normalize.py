import numpy as np
from numba import jit

@jit(nopython=True, parallel=True)
def norm_I(I: np.ndarray) -> np.ndarray:
    imin, imax = min(I), max(I)
    I_N = (I - imin) / (imax - imin)
    return I_N
