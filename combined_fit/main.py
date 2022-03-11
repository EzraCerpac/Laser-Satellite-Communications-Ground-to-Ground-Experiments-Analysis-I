import numpy as np
import pickle
from matplotlib import pyplot as plt

from combined_fit.angular_jitter_fit import plot_angular_jitter_dist, fit_beta_to_hist, calc_sigma
from combined_fit.scintillation import integrate_scint_index
from info_plots.norm_I_hist import norm_I_hist


def estimate_sigma(I: np.ndarray, plot: bool):
    res = 1001
    usable_indices = res // 5
    ii = np.linspace(0, 1, res)
    residu = residu_angular_jitter(I, res, plot)[:usable_indices]
    beta, residu = fit_beta_to_hist(residu, ii[:usable_indices])
    if plot:
        plot_angular_jitter_dist(residu, beta, ii[:usable_indices])
    sigma = calc_sigma(beta, 11e-6)
    return sigma


def residu_angular_jitter(I: np.ndarray, res: int = 101, plot: bool = False) -> np.ndarray:
    ii = np.linspace(0, 1, res + 1)[1:]
    plt.plot(ii, p_sc := integrate_scint_index(I, ii), label='integrated scintillation')
    yy = norm_I_hist(I, density=True, bins=res + 1)[1:]
    residu = yy / p_sc
    if plot:
        plt.plot(ii, residu, label='residu angular jitter')
        plt.legend()
        plt.show()
    else:
        plt.clf()
    return residu


def main():
    with open('../Data/DFs/data11/off1.pickle', 'rb') as f:
        data = pickle.load(f)
    I = np.array(data)
    estimate_sigma(I, True)


if __name__ == '__main__':
    main()
