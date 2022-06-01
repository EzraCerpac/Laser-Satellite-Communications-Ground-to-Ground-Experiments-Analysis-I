from pprint import pprint
from typing import Callable

import numpy as np


def cost(func: Callable, x: np.ndarray, y: np.ndarray, popt) -> float:
    f = func(x, *popt)
    # f = fix_NaN(f)
    val = np.sum(np.square(np.subtract(y, f))) / (max(y) if max(y) > 0 else 1)
    return val


def fix_NaN(x: np.ndarray) -> np.ndarray:
    """
    Replace NaN's in x with interpolated values
    """
    # find NaN's
    nan_indices = np.argwhere(np.isnan(x))
    # make a copy of x
    xx = x.copy()
    # interpolate
    for i in nan_indices:
        if i[0] == 0:
            xx[i[0]] = xx[i[0] + 1]
        elif i[0] == len(x) - 1:
            xx[i[0]] = xx[i[0] - 1]
        else:
            xx[i[0]] = xx[i[0] - 1] + (xx[i[0] + 1] - xx[i[0] - 1]) / 2
    return xx
