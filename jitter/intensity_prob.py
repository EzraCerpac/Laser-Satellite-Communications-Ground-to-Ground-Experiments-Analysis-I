from dataclasses import dataclass
from typing import Any

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import beta


@dataclass
class IntensityDistribution:
    intensities: np.ndarray
    w_0: float
    b: float = 1

    @property
    def norm_I(self) -> np.ndarray:
        return self.intensities / max(self.intensities)

    def fit(self) -> list:
        return [beta.fit(self.norm_I, fb=1, floc=0, fscale=1)]  # TODO: fix error: Invalid values in `data`.
        # Maximum likelihood estimation with 'beta' requires that 0 < (x - loc)/scale  < 1 for each x in `data`.

    @property
    def sigma(self) -> float:
        beta1 = self.a
        sigma1 = np.sqrt(self.w_0 ** 2 / (4 * beta1))
        return sigma1

    @property
    def a(self) -> float:
        return self.fit()[0]

    def plot(self):
        plt.hist(self.norm_I)
        I = np.linspace(0, 1, 101)
        plt.plot(I, beta.pdf(I, self.a, self.b), 'r-', label='beta pdf')
        plt.legend()
        plt.show()
