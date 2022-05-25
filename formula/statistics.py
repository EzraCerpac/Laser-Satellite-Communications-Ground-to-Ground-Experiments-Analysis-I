import numpy as np


def cost(func, x, y, popt) -> float:
    f = func(x, *popt)
    return np.sum((y - f) ** 2) / max(f)
