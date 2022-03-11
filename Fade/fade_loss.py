import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from scipy import interpolate, \
    quad

def Ap_Av(k, D, L):
    """

    :param k: Wave Number
    :param D: Diameter of Beam
    :param L: Distance to Transmitter
    :return: Aperature Averaging Factor
    """
    return (1 + 1.062 * ((k * D ** 2) / (4 * L))) ** (7 / 6)


def Sigma_I(Sigma_R2):
    """

    :param Sigma_R: Rytov Index
    :return: Intensity Scintillation Index
    """
    return np.exp((0.49 * Sigma_R2) / (1 + 1.11 * Sigma_R2 ** (6 / 5)) + (0.51 * Sigma_R2) / (
                1 + 0.69 * Sigma_R2 ** (6 / 5)) ** (5 / 6)) - 1


def Sigma_R2(Cn, k, L):
    """

    :param Cn: Refractive Index
    :param k: Wave Number
    :param L: Distance to Transmitter
    :return: Rytov Index
    """
    return 1.23 * Cn ** 2 * k ** (7 / 6) * L ** (11 / 6)


def Sigma_P(A, Sigma_I):
    """

    :param A: Aperture averaging factor
    :param Sigma_I: Intensity Scintillation Index
    :return: Power Scintillation Index
    """
    return A * Sigma_I


def p_P(P_RX, Sigma_P, P0):
    """

    :param P_RX:
    :param Sigma_P:
    :param P0:
    :return: Probability Distribution
    """
    a = 1 / (P_RX * (2 * np.pi * np.log(Sigma_P + 1)) ** (1 / 2))
    b = - ((np.log(P_RX / P0) + 0.5 * np.log(Sigma_P + 1)) ** 2) / (2 * np.log(Sigma_P + 1))
    return a * np.exp(b)


def test_curve(x, a, b):

    part1 = 1 / (x * (2 * np.pi * np.log(a + 1)) ** (1 / 2))
    part2 = - ((np.log(x / b) + 0.5 * np.log(x + 1)) ** 2) / (2 * np.log(x + 1))
    return part1 * np.exp(part2)




# k is 2*pi/lambda, D is reciever diameter
folder = Path('CSV')
datacn = pd.read_csv(folder / 'Cnprofile', names=['z-dist', 'height', 'cn2'], skiprows=1)

print(datacn.height[2])

Lambda = 1550e-9
Cn = 0.033
L = 10000
D = 3.45
P0 = 1000
k = 2 * np.pi / Lambda

A = Ap_Av(k, D, L)
SigR = Sigma_R2(Cn, k, L)
SigI = Sigma_I(SigR)
SigP = Sigma_P(A, SigI)

PRl = np.linspace(0, 101)
pPl = p_P(PRl, SigP, P0)
# pPl = test_curve(PRl, 3, 50)

plt.plot(PRl, pPl)
plt.show()

