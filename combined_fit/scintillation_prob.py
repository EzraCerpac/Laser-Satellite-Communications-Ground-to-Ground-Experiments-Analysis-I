from __future__ import annotations

import pickle

import numpy as np
from matplotlib import pyplot as plt
from scipy import integrate


def main():
    with open('../Data/DFs/data11/off1.pickle', 'rb') as f:
        data = pickle.load(f)
    I = np.array(data)
    ii = np.linspace(0, 1, 1001)
    probs = calc_probs(I, ii)

    plt.plot(ii, probs)
    plt.show()


def calc_probs(I: np.ndarray, ii: np.ndarray) -> np.ndarray:
    with open('../Data/DFs/Cn.pickle', 'rb') as f:
        Cn = pickle.load(f)

    zz = np.array(Cn['z-distance'])
    C_n2 = np.array(Cn['Cn^2'])

    labda = 1e-6  # Wavelength (unknown)

    sigma_R2 = rytov_index(k(labda), zz, C_n2)
    sigma_I2 = scintillation_index(sigma_R2)

    norm_I = I / max(I)
    I_0 = norm_I.mean()
    return probability_dist(ii, I_0, sigma_I2)  # return array


def probability_dist(I: float | np.ndarray, I_0: float, sigma_I2: float) -> float | np.ndarray:
    return 1 / (I * sigma_I2 * np.sqrt(2 * np.pi)) * np.exp(
        - (np.log(I / I_0) + 0 + sigma_I2 / 2) ** 2 / (2 * sigma_I2)
    )


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


if __name__ == '__main__':
    main()
