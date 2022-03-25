import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from combined_fit.scintillation import calc_probs
from info_plots.norm_I_hist import norm_I_hist


def residu_angular_jitter(I: np.ndarray, res: int = 101, plot: bool = False) -> np.ndarray:
    ii = np.linspace(0, 1, res + 1)[1:]

    # TODO: choose between the 2 versions below
    # plt.plot(ii, p_sc := integrate_scint_index(I, ii), label='integrated scintillation')
    Cn = pd.read_pickle('Data/DFs/Cn.pickle')
    plt.plot(ii, p_sc := calc_probs(I, ii), label='scintillation')
    plt.ylim(0, 1.2 * np.max(p_sc))

    yy = norm_I_hist(I, density=True, bins=res + 1, plot=False)[1:]
    residu = yy / p_sc
    if plot:
        plt.plot(ii, residu, label='residu angular jitter')
        # plt.ylim((0, 1.2 * max(residu)))
    # else:
    #     plt.clf()
    return residu
