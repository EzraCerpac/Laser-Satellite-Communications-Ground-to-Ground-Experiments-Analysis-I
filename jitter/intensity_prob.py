from dataclasses import dataclass, field

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import beta


@dataclass
class IntensityDistribution:
    intensities: np.ndarray
    w_0: float = field(default=1.)
    b: float = 1

    @property
    def norm_I(self) -> np.ndarray:
        return self.intensities / (max(self.intensities) + 1e-3)

    def fit(self) -> list:
        return [beta.fit(self.norm_I, fb=1, floc=0, fscale=1)]

    @property
    def sigma(self) -> float:
        beta1 = self.a
        sigma1 = np.sqrt(self.w_0 ** 2 / (4 * beta1))
        return sigma1

    @property
    def a(self) -> float:
        return self.fit()[0]

    def plot(self):
        plt.hist(self.intensities, density=True, label='data')
        I = np.linspace(beta.ppf(0.01, self.a, self.b), beta.ppf(0.99, self.a, self.b), 101)
        plt.plot(I, beta.pdf(I, self.a, self.b), 'r-', label='beta pdf')
        plt.legend()
        plt.show()
