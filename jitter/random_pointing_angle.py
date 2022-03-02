from dataclasses import dataclass, field

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import rayleigh


class PointingProbability:
    def __init__(self, sigma: float):
        self.sigma = sigma
        self.alpha = np.linspace(0., 0.0025, 101)
        self.prob = rayleigh.pdf(self.alpha, scale=sigma)

    def plot(self):
        plt.plot(self.alpha, self.prob)
        plt.legend()
        plt.show()
