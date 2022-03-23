import numpy as np
from scipy import integrate


def rytov_index(k, zz: np.ndarray, C_n2: np.ndarray) -> float:
    coef = 2.25 * k ** (7 / 6)
    integrand = [C_n2[i] * (zz[-1] - z) ** (5 / 6) for i, z in enumerate(zz)]
    integral = integrate.simpson(integrand, zz)
    return coef * integral


def rytov_index_romb(k, zz: np.ndarray, C_n2: np.ndarray) -> float:
    coef = 2.25 * k ** (7 / 6)
    # integrand = lambda i: C_n2[i] * (zz[-1] - zz[i]) ** (5 / 6)
    integrand = [C_n2[i] * (zz[-1] - z) ** (5 / 6) for i, z in enumerate(zz)]
    integral = integrate.cumtrapz(integrand, zz)
    return coef * integral


def rytov_index_const(k: float, L: float, C_n2: float) -> float:
    return 1.23 * C_n2 * k ** (7 / 6) * L ** (11 / 6)


def scintillation_index(sigma_R2) -> float:
    return np.exp(
        0.49 * sigma_R2 / (1 + 1.11 * sigma_R2 ** (6 / 5)) ** (7 / 6) +
        0.51 * sigma_R2 / (1 + 0.69 * sigma_R2 ** (6 / 5)) ** (5 / 6)
    ) - 1
