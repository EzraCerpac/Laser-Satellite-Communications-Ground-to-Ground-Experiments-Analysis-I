import logging
import multiprocessing as mp
import os
import time
from os import path
from typing import Dict

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import lognorm, invgamma

from Model.with_beta import combined_dist, combined_dist_gamma
from conf.data import Data
from plotting.norm_I_hist import norm_I_hist

log = logging.getLogger(__name__)

LW = 2


def plot_combined(
        results: Dict[int, Dict[bool, Dict[int, Dict[str, Dict[str, float]]]]],
        save: bool = False,
        dir: str = time.strftime("%d-%m-%Y_%H-%M")
) -> None:
    log.info("Starting plot sequence")
    pool = mp.Pool(mp.cpu_count())
    plottings = []
    for set, modes in results.items():
        for mode, nums in modes.items():
            for num, funcs in nums.items():
                plottings.append(pool.apply_async(_plot_one, args=(funcs, mode, num, set, save, dir)))
    [plot.get() for plot in plottings]
    pool.close()
    log.info("Finished plots")


def _plot_one(funcs: dict, mode: bool, num: int, set: int, save: bool, dir: str) -> None:
    linestyles = ['o-', 'D-', '^-', 's-', '*-', 'P-']
    try:
        fig, ax = plt.subplots(figsize=(7, 5))
        # plt.title(f'Histogram and Probs of {set}urad, mode {"on" if mode else "off"}: {num}')
        plt.xlabel(r'$I_{norm}$')
        plt.ylabel(r'PDF')
        norm_I_hist(np.array(Data(set, mode, num).df), bins=300)
        xx = np.linspace(0, 1, 101)
        # log.info(f'Plotting set {set}, modes {"on" if mode else "off"}, {num}')
        for func, values in funcs.items():
            if func == 'lognormal in beta':
                ax.plot(
                    xx,
                    combined_dist(xx, values['alpha'], values['beta']), linestyles.pop(), markevery=7,
                    label=f'{func} (α={values["alpha"]:.3g}, β={values["beta"]:.3g}, '
                          f'MSE={values["standard div"]:.3g})',
                    # linewidth=LW
                )
            if func == 'gamma in beta':
                ax.plot(
                    xx,
                    combined_dist_gamma(xx, values['alpha'], values['beta']), linestyles.pop(), markevery=7,
                    label=f'{func} (α={values["alpha"]:.3g}, β={values["beta"]:.3g}, '
                          f'MSE={values["standard div"]:.3g})',
                    # linewidth=LW
                )
            if func == 'lognormal':
                plt.plot(
                    xx,
                    lognorm.pdf(xx, values['skew'], values['pos']), linestyles.pop(), markevery=7,
                    label=f'{func} (σ={values["skew"]:.3g}, μ={values["pos"]:.3g}, '
                          f'MSE={values["standard div"]:.3g})',
                    # linewidth=LW
                )
            if func == 'inv gamma':
                plt.plot(
                    xx,
                    invgamma.pdf(xx, values['a'], values['pos']), linestyles.pop(), markevery=7,
                    label=f'{func} (α={values["a"]:.3g}, β={values["pos"]:.3g}, '
                          f'MSE={values["standard div"]:.3g})',
                    # linewidth=LW
                )
            if func == 'lognormal full fit':
                plt.plot(xx, combined_dist(xx, values['alpha'], values['beta'], values['sigma_i'], full_fit=True),
                         linestyles.pop(), markevery=7,
                         label=f'{func} (α={values["alpha"]:.3g}, β={values["beta"]:.3g}, $\sigma_i$={values["sigma_i"]:.3g}'
                               f', MSE={values["standard div"]:.3g})',
                         # linewidth=LW
                         )
            if func == 'gamma full fit':
                ax.plot(
                    xx,
                    combined_dist_gamma(xx, values['alpha'], values['beta'], values['a'], values['b'], full_fit=True),
                    linestyles.pop(), markevery=7,
                    label=f'{func} (α={values["alpha"]:.3g}, β={values["beta"]:.3g}, a={values["a"]:.3g}, b={values["b"]:.3g}'
                          f', MSE={values["standard div"]:.3g})',
                    # linewidth=LW
                )
        plt.xlim(0, 1)
        plt.legend()
        if save:
            dir = 'Plots/' + dir
            if not path.exists(dir):
                os.makedirs(dir)
            plt.savefig(f"{dir}/set{set}_{mode}_{num}.pdf")
            log.info(f"Saved plot to {dir}/set{set}_{mode}_{num}.pdf")
        else:
            plt.show()
    except Exception as e:
        log.error(f'Failed to plot set{set} {mode} {num}: {e}')
