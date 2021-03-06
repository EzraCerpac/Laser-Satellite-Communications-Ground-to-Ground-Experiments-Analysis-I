import numpy as np
from scipy.integrate import quad
from scipy.special import erfc

from misc.formula.basic import beta

BER = lambda Q: 0.5 * erfc(Q / np.sqrt(2))


def average_BER(Q, w_sigma):
    integral = quad(
        lambda I: I ** (beta(w_sigma) - 1) * erfc(I * Q * (beta(w_sigma) + 1) / (np.sqrt(2) * beta(w_sigma))), 0, 1)
    return (Q * (beta(w_sigma) + 1)) / 2 * integral[0]
