import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from combined_fit.angular_jitter_fit_beta import estimate_sigma
from combined_fit.scintillation import integrate_scint_index
from info_plots.norm_I_hist import norm_I_hist


def residu_angular_jitter(I: np.ndarray, res: int = 101, plot: bool = False) -> np.ndarray:
    ii = np.linspace(0, 1, res + 1)[1:]
    plt.plot(ii, p_sc := integrate_scint_index(I, ii), label='integrated scintillation')
    yy = norm_I_hist(I, density=True, bins=res + 1)[1:]
    residu = yy / p_sc
    if plot:
        plt.plot(ii, residu, label='residu angular jitter')
    # else:
    #     plt.clf()
    return residu


def main():
    data = pd.read_pickle('../Data/DFs/data11/off1.pickle')
    I = np.array(data)
    print(estimate_sigma(I, 11e-6, 301, 0.25, plot=True))
    plt.xlim(0, 0.5)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
