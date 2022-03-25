import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.integrate import quad
from scipy.optimize import curve_fit
from scipy.stats import rv_continuous

from combined_fit.angular_jitter_fit_beta import beta_func
from combined_fit.indices import scintillation_index, rytov_index
from combined_fit.scintillation import probability_dist
from formula.jitter import k
from info_plots.norm_I_hist import norm_I_hist

Cn = pd.read_pickle('Data/DFs/Cn.pickle')
zz = np.array(Cn['z-distance'])
C_n2 = np.array(Cn['Cn^2'])


class CombinedFit(rv_continuous):
    # def __init__(self, **kwargs):
    #     super(CombinedFit, self).__init__(*kwargs)

    def _pdf(self, X, beta):
        return [quad(lambda I: beta_func(I, beta[0]) * probability_dist(
            x, I, scintillation_index(rytov_index(
                k(labda), zz, C_n2
            ))), 0, 1)[0] for x in X] if hasattr(X, '__iter__') \
            else quad(lambda I: beta_func(I, beta) * probability_dist(
            X, I, scintillation_index(rytov_index(
                k(labda), zz, C_n2
            ))), 0, 1)[0]


beta = 3
labda = 1550e-9


def main_colors():
    ii = np.linspace(1e-10, 4, 1000)
    II = np.linspace(0, 1, 1000)
    ff = np.zeros(len(ii))
    for i in II:
        f = beta_func(i, beta) * probability_dist(
            ii, i, scintillation_index(rytov_index(
                k(labda), zz, C_n2
            )))
        plt.plot(ii, f)
        ff += f
    ff /= len(II)
    plt.plot(ii, ff, color='black', linewidth=4)
    plt.show()

    print(np.sum(ff) * (ii[1] - ii[0]))


def main():
    ii = np.linspace(1e-10, 4, 1000)
    ff = [quad(lambda I: beta_func(I, beta) * probability_dist(
        i, I, scintillation_index(rytov_index(
            k(labda), zz, C_n2
        ))), 0, 1)[0] for i in ii]
    plt.plot(ii, ff, color='black', linewidth=4)
    plt.show()

    print(np.sum(ff) * (ii[1] - ii[0]))


def combined_dist(i: float, beta: float, scale: float = 1):
    return quad(lambda I: beta_func(I, beta) * probability_dist(
        i, I, scintillation_index(rytov_index(
            k(labda), zz, C_n2
        ))), 0, 1)[0] / scale


def main2(irradiance):
    yy = norm_I_hist(irradiance, bins=100)
    xx = np.linspace(0, 1, len(yy))
    p_opt, p_error = curve_fit(CombinedFit().pdf, xx, yy, p0=[2])
    beta, scale = p_opt
    plt.plot(xx, [CombinedFit().pdf(x, beta) for x in xx])
    plt.show()


if __name__ == '__main__':
    main2()
