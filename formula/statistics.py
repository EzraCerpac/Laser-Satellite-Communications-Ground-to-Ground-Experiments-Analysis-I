import numpy as np


def MSE(func, x, y, popt) -> float:
    return np.mean((y - func(x, *popt)) ** 2)
