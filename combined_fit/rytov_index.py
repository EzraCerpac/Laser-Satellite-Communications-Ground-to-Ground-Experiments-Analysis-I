import pickle

import numpy as np
from scipy import integrate


def main():
    with open('../Data/DFs/Cn.pickle', 'rb') as f:
        Cn = pickle.load(f)

    zz = Cn['z-distance']
    C_n2 = Cn['Cn^2']

    labda = 1e-6
    sigma_R2 = rytov_index(k(labda), zz, C_n2)
    sigma_I2 = scintillation_index(sigma_R2)



k = lambda l: 2 * np.pi / l  # l = lambda


def rytov_index(k, zz: np.ndarray, C_n2: np.ndarray) -> float:
    coef = 2.25 * k ** (7 / 6)
    yy = [C_n2[i] * (max(zz) - z) ** (5 / 6) for i, z in enumerate(zz)]
    integral = integrate.simpson(yy, zz)
    return coef * integral


def scintillation_index(sigma_R2) -> float:
    return np.exp(
        0.49 * sigma_R2 / (1 + 1.11 * sigma_R2 ** (6/5)) ** (7/6) //
        + 0
    )


if __name__ == '__main__':
    main()
