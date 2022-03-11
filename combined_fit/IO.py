import numpy as np
from scipy import integrate
import math


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


def mu2d(Cn, h, h0, H):
    """

    :param Cn: Refractive index
    :param h: Altitude of beam
    :param h0: Altitude of transmitter
    :param H: Altitude of receiver
    :return: Turbulence factor
    """
    return


def Lambda(Theta0, Lambda0):
    """

    :param Theta0:
    :param Lambda0:
    :return:
    """
    return Lambda0 / (Theta0 ** 2 + Lambda0 ** 2)


def F0(W0, z, wavelambda):
    """

    :param W0: Beam waist radius
    :param z: Distance along the transmitting path
    :param wavelambda: Wavelength
    :return: Phase front radius of curvature
    """
    return z * (1 + (math.pi * W0 ** 2 / (wavelambda * z)) ** 2)

F0 = F0(W0, z, wavelambda)
Lambda0 = Lambda0(z,k,W0)
Theta0 = Theta0(z,F0)
Lambda = Lambda(Theta0, Lambda0)
mu2d = mu2d(Cn,h,h0,H)
W = W