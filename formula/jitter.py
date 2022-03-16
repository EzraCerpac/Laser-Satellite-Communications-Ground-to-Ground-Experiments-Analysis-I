import numpy as np


def calc_sigma(beta: float, w_0: float) -> float:
    sigma = np.sqrt(w_0 ** 2 / (4 * beta))
    return sigma

def k(labda: float) -> float: return 2 * np.pi / labda  # labda = lambda
