import math
from scipy import stats

from combined_fit.IO import I0


def gamma_gamma(alpha, beta, I, K_alpha):
    return ((2 * (alpha * beta) ** ((alpha + beta) / 2)) / (stats.gamma(alpha) * stats.gamma(beta) * I)) * ((I / I0(W0,WLT)) ** ((alpha + beta) / 2)) * K_alpha

def alpha(Rytov):
    return math.e ** (0.49 * Rytov ** 2 / (1 + 1.11 * Rytov ** (12 / 5)) ** (7 / 6)) - 1

def beta(Rytov):
    return math.e ** (0.51 * Rytov ** 2 / (1 + 0.69 * Rytov ** (12 / 5)) ** (5 / 6)) - 1
