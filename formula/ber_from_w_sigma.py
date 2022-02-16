import numpy as np
from scipy.integrate import quad
from scipy.special import erfc

from formula.basic import beta


def average_BER(Q, w_sigma):
    integral = quad(
        lambda I: I ** (beta(w_sigma) - 1) * erfc(I * Q * (beta(w_sigma) + 1) / (np.sqrt(2) * beta(w_sigma))), 0, 1)
    return (Q * (beta(w_sigma) + 1)) / 2 * integral[0]
