import logging
import multiprocessing as mp
import os
import time
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

from Model.with_beta import combined_dist_gamma, combined_dist
from combined_fit.angular_jitter_fit_gamma import gamma_gamma
from combined_fit.scintillation import probability_dist
from conf.data import Data
from plotting.norm_I_hist import norm_I_hist

log = logging.getLogger(__name__)

linestyles = ['o-', 'D-', '^-', 's-', '*-', 'P-']


def build_up_plots(results: Dict[int, Dict[bool, Dict[int, Dict[str, Dict[str, float]]]]], func: str,
                   save: bool = False):
    log.info("Starting plot sequence for gamma and beta")
    pool = mp.Pool(mp.cpu_count())
    plottings = []
    for set, modes in results.items():
        for mode, nums in modes.items():
            for num, funcs in nums.items():
                if set == 18:
                    # if mode is True and num == 4:
                    plottings.append(pool.apply_async(_gamma_beta, args=(func, funcs[func], mode, num, set, save, dir)))
    [plot.get() for plot in plottings]
    pool.close()
    log.info("Finished plots")


def _gamma_beta(func: str, values: dict, mode: bool, num: int, set: int, save: bool, dir: str) -> None:
    try:
        fig, ax = plt.subplots(figsize=(7, 5))
        # plt.title(f'Histogram and Probs of {set}urad, mode {"on" if mode else "off"}: {num}')
        plt.xlabel(r'$I_{norm}$')
        plt.ylabel(r'PDF')
        ii = norm_I_hist(np.array(Data(set, mode, num).df), bins=300)
        xx = np.linspace(0, 1, 101)
        # log.info(f'Plotting set {set}, modes {"on" if mode else "off"}, {num}')
        if func == 'lognormal in beta':
            plt.plot(xx,
                     combined_dist(xx, values['alpha'], values['beta']),
                     linestyles.pop(), markevery=7,
                     label=f'combined {func}'
                     )
            plt.plot(xx, beta.pdf(xx, values['alpha'], values['beta']), linestyles.pop(), markevery=7,
                     label=f'beta'
                     )
            plt.plot(xx, probability_dist(xx, 0.5, 1.2115807486724068), linestyles.pop(), markevery=7,
                     label=f'lognormal'  # maybe I_0 should be ii.mean()
                     )
        if func == 'gamma in beta':
            plt.plot(xx,
                     combined_dist_gamma(xx, values['alpha'], values['beta']),
                     linestyles.pop(), markevery=7,
                     label=f'combined {func}'
                     )
            plt.plot(xx, beta.pdf(xx, values['alpha'], values['beta']), linestyles.pop(), markevery=7,
                     label=f'beta'
                     )
            plt.plot(xx, gamma_gamma(xx, values['alpha'], values['beta']), linestyles.pop(), markevery=7,
                     label=f'lognormal'  # maybe I_0 should be ii.mean()
                     )
        if func == 'gamma full fit':
            plt.plot(xx,
                     combined_dist_gamma(xx, values['alpha'], values['beta'], values['a'], values['b'], full_fit=True),
                     linestyles.pop(), markevery=7,
                     label=f'combined gamma in beta'
                     )
            plt.plot(xx, beta.pdf(xx, values['alpha'], values['beta']), linestyles.pop(), markevery=7,
                     label=f'beta'
                     )
            plt.plot(xx, gamma_gamma(xx, values['a'], values['b']), linestyles.pop(), markevery=7, label=f'gamma')
        if func == 'lognormal full fit':
            plt.plot(xx,
                     combined_dist(xx, values['alpha'], values['beta'], full_fit=True),
                     linestyles.pop(), markevery=7,
                     label=f'combined {func}'
                     )
            plt.plot(xx, beta.pdf(xx, values['alpha'], values['beta']), linestyles.pop(), markevery=7,
                     label=f'beta'
                     )
            plt.plot(xx, probability_dist(xx, 0.5, values['sigma_i']), linestyles.pop(), markevery=7,
                     label=f'lognormal'  # maybe I_0 should be ii.mean()
                     )
        plt.legend()
        if save:
            dir = f'Plots/{time.strftime("%d-%m-%Y_%H-%M")}Gamma_Beta_Comparison'
            if not os.path.exists(dir):
                os.makedirs(dir)
            plt.savefig(f'{dir}/{set}urad_{mode}_{num}.png')
            log.info(f'Saved plot to {dir}/{set}urad_{mode}_{num}.png')
        else:
            plt.show()
    except Exception as e:
        log.error(f'Error in {set}urad {mode} {num}: line {e.__traceback__.tb_lineno}')
