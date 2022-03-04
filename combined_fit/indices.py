from __future__ import annotations

import numpy as np
from scipy import integrate


def k(l): return 2 * np.pi / l  # l = lambda


def rytov_index(k, zz: np.ndarray, C_n2: np.ndarray) -> float:
    coef = 2.25 * k ** (7 / 6)
    yy = [C_n2[i] * (zz[-1] - z) ** (5 / 6) for i, z in enumerate(zz)]
    integral = integrate.simpson(yy, zz)
    return coef * integral


def scintillation_index(sigma_R2) -> float:
    return np.exp(
        0.49 * sigma_R2 / (1 + 1.11 * sigma_R2 ** (6 / 5)) ** (7 / 6) +
        0.51 * sigma_R2 / (1 + 0.69 * sigma_R2 ** (6 / 5)) ** (5 / 6)
    ) - 1
