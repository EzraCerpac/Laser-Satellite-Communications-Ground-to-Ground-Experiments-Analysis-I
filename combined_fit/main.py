import pickle

import numpy as np
from matplotlib import pyplot as plt

from combined_fit.scintillation import integrate_scint_index
from info_plots.norm_I_hist import norm_I_hist


def main():
    with open('../Data/DFs/data11/off1.pickle', 'rb') as f:
        data = pickle.load(f)
    I = np.array(data)
    residu = residu_angular_jitter(I, plot=True)
    # beta = calc_beta(residu)  # TODO: make working
    # plot_angular_jitter_dist(residu, beta)
    # plt.show()


def residu_angular_jitter(I: np.ndarray, plot: bool = False) -> np.ndarray:
    ii = np.linspace(0, 1, 101)[1:]
    plt.plot(ii, p_sc := integrate_scint_index(I, ii), label='integrated scintillation')
    yy = norm_I_hist(I, density=True, bins=101)[1:]
    residu = yy / p_sc
    if plot:
        plt.plot(ii, residu, label='residu angular jitter')
        plt.legend()
        plt.show()
    else:
        plt.clf()
    return residu


if __name__ == '__main__':
    main()
