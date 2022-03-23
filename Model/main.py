import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from combined_fit.angular_jitter_fit_beta import beta_func
from combined_fit.indices import scintillation_index, rytov_index, rytov_index_const
from combined_fit.scintillation import probability_dist
from formula.jitter import k

beta = 3
labda = 1550e-9

Cn = pd.read_pickle('../Data/DFs/Cn.pickle')
zz = np.array(Cn['z-distance'])
C_n2 = np.array(Cn['Cn^2'])


def main():
    ii = np.linspace(1e-10, 1, 1000)
    II = np.linspace(1e-10, 1, 50)
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


def test():
    ii = np.linspace(1e-18, 1, 1000)
    ff = probability_dist(
        ii, 0.5, scintillation_index(rytov_index_const(
            k(labda), max(zz), C_n2.mean()
        )))
    print(np.sum(ff) * (ii[1] - ii[0]))


if __name__ == '__main__':
    test()
