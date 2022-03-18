import math
import numpy as np
import pandas as pd
from scipy import integrate

from formula.jitter import k


def I0(W0, WLT):
    """

    :param W0: Beam radius
    :param WLT: Long-term spot size
    :return: Mean irradiance at beamcenter
    """
    return W0 ** 2 / WLT ** 2


def WLT(W, mu2d, Lambda, k, H, h0):
    """

    :param W: Diffractive beam radius
    :param mu2d: Turbulence factor
    :param Lambda:
    :param k: Wavenumber
    :param H: Altitude of receiver
    :param h0: Altitude of transmitter
    :return: Long-term spot size
    """
    return W * (1 + 4.35 * mu2d * Lambda ** (5 / 6) * k ** (7 / 6) * (H - h0) ** (5 / 6) * (
            (300 ** 2 + 10000 ** 2) ** (1 / 2) / 300) ** (11 / 6)) ** (1 / 2)


def W(W0, Theta0, Lambda0):
    """

    :param W0: Beam radius
    :param Theta0:
    :param Lambda0:
    :return: Diffractive beam radius
    """
    return W0 * (Theta0 ** 2 + Lambda0 ** 2) ** (1 / 2)


def Theta0(z, F0):
    """

    :param z: Distance to transmitter
    :param F0: Phase front radius of curvature
    :return:
    """
    return 1 - z / F0


def Lambda0(z, k, W0):
    """

    :param z: Distance to transmitter
    :param k: Wavenumber
    :param W0: Beam radius
    :return:
    """
    return 2 * z / (k * W0 ** 2)


def mu2d(hh: np.ndarray, C_n2: np.ndarray) -> float:
    """
    Compute the mu_2d by integration.
    Not working, because hh isn't in order, so no integration is possible.
    Fix is plugging in zz instead of hh. Probably does not work.
    TODO: check effect of using zz or rr instead of hh.
    """
    yy = [C_n2[i] * ((h - hh[0]) / (hh[-1] - hh[0])) ** (5 / 3) for i, h in enumerate(hh)]
    integral = integrate.simpson(yy, hh)
    return integral


def Lambda(Theta0, Lambda0):
    """

    :param Theta0:
    :param Lambda0:
    :return:
    """
    return Lambda0 / (Theta0 ** 2 + Lambda0 ** 2)


def F0(W0, zi, wavelambda):
    """

    :param W0: Beam waist radius
    :param zi: Distance along the transmitting path
    :param wavelambda: Wavelength
    :return: Phase front radius of curvature
    """
    return zi * (1 + (math.pi * W0 ** 2 / (wavelambda * zi)) ** 2)


def main():
    Cn = pd.read_pickle('../Data/DFs/Cn.pickle')
    zz = np.array(Cn['z-distance'])
    C_n2 = np.array(Cn['Cn^2'])
    hh = np.array(Cn['altitude'])
    F0_inf = math.inf
    W0 = 11e-6  # random
    wavelambda = 1550e-9
    io = I0(
        W0,
        WLT(
            W(
                W0,
                Theta0(zz[-1], F0_inf),
                Lambda0(zz[-1], k(wavelambda), W0)
            ),
            mu2d(zz, C_n2),
            Lambda(
                Theta0(zz[-1], F0_inf),
                Lambda0(zz[-1], k(wavelambda), W0)
            ),
            k(wavelambda),
            hh[-1],
            hh[0]
        )
    )
    return io


if __name__ == '__main__':
    print(main())