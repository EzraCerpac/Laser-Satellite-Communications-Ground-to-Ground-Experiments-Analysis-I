import logging
import multiprocessing as mp
import os
import time
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

from Model.with_beta import combined_dist_gamma
from combined_fit.angular_jitter_fit_gamma import gamma_gamma
from conf.data import Data
from plotting.norm_I_hist import norm_I_hist

log = logging.getLogger(__name__)

linestyles = ['o-', 'D-', '^-', 's-', '*-', 'P-']


def build_up_plots(results: Dict[int, Dict[bool, Dict[int, Dict[str, Dict[str, float]]]]], save: bool = False):
    log.info("Starting plot sequence for gamma and beta")
    pool = mp.Pool(mp.cpu_count())
    plottings = []
    for set, modes in results.items():
        for mode, nums in modes.items():
            for num, funcs in nums.items():
                if set == 18:
                    if mode == True and num == 4:
                        plottings.append(pool.apply_async(_gamma_beta, args=(funcs, mode, num, set, save, dir)))
    [plot.get() for plot in plottings]
    pool.close()
    log.info("Finished plots")


def _gamma_beta(funcs: dict, mode: bool, num: int, set: int, save: bool, dir: str) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    # plt.title(f'Histogram and Probs of {set}urad, mode {"on" if mode else "off"}: {num}')
    plt.xlabel(r'$I_{norm}$')
    plt.ylabel(r'PDF')
    norm_I_hist(np.array(Data(set, mode, num).df), bins=300)
    xx = np.linspace(0, 1, 101)
    # log.info(f'Plotting set {set}, modes {"on" if mode else "off"}, {num}')
    for func, values in funcs.items():
        if func == 'gamma full fit':
            print(values)
            plt.plot(xx,
                     combined_dist_gamma(xx, values['alpha'], values['beta'], values['a'], values['b'], full_fit=True),
                     linestyles.pop(), markevery=7,
                     label=f'combined gamma in beta'
                     )
            plt.plot(xx, beta.pdf(xx, values['alpha'], values['beta']), linestyles.pop(), markevery=7,
                     label=f'beta'
                     )
            plt.plot(xx, gamma_gamma(xx, values['a'], values['b']), linestyles.pop(), markevery=7, label=f'gamma')
    plt.legend()
    if save:
        dir = f'Plots/{time.strftime("%d-%m-%Y_%H:%M")}Gamma_Beta_Comparison'
        if not os.path.exists(dir):
            os.makedirs(dir)
        plt.savefig(f'{dir}/{set}urad_{mode}_{num}.png')
        log.info(f'Saved plot to {dir}/{set}urad_{mode}_{num}.png')
    else:
        plt.show()
