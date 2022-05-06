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


def plot_combined(
        results: Dict[int, Dict[bool, Dict[int, Dict[str, Dict[str, float]]]]],
        save: bool = False,
        dir: str = time.strftime("%d/%m-%H:%M")
) -> None:
    log.info("Starting plot sequence")
    pool = mp.Pool(mp.cpu_count())
    plottings = []
    for set, modes in results.items():
        for mode, nums in modes.items():
            for num, funcs in nums.items():
                plottings.append(pool.apply_async(_plot_one, args=(funcs, mode, num, set, save)))
    [plot.get() for plot in plottings]
    pool.close()
    log.info("Finished plots")


def _plot_one(funcs: dict, mode: bool, num: int, set: int, save: bool) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.title(f'Histogram and Probs of {set}urad, mode {"on" if mode else "off"}: {num}')
    norm_I_hist(np.array(Data(set, mode, num).df), bins=300)
    xx = np.linspace(0, 1, 101)
    log.info(f'Plotting set {set}, modes {"on" if mode else "off"}, {num}')
    for func, values in funcs.items():
        if func == 'lognormal in beta':
            ax.plot(
                xx,
                combined_dist(xx, values['alpha'], values['beta']),
                label=f'{func} (α={values["alpha"]:.2f}, β={values["beta"]:.2f}, '
                      f'MSE={values["standard div"]:.2f})'
            )
        if func == 'gamma in beta':
            ax.plot(
                xx,
                combined_dist_gamma(xx, values['alpha'], values['beta']),
                label=f'{func} (α={values["alpha"]:.2f}, β={values["beta"]:.2f}, '
                      f'MSE={values["standard div"]:.2f})'
            )
        if func == 'lognormal':
            plt.plot(
                xx,
                lognorm.pdf(xx, values['skew'], values['pos']),
                label=f'{func} (σ={values["skew"]:.2f}, μ={values["pos"]:.2f}, '
                      f'MSE={values["standard div"]:.2f})'
            )
        if func == 'inv gamma':
            plt.plot(
                xx,
                invgamma.pdf(xx, values['a'], values['pos']),
                label=f'{func} (α={values["a"]:.2f}, β={values["pos"]:.2f}, '
                      f'MSE={values["standard div"]:.2f})'
            )
        if func == 'lognormal full fit':
            plt.plot(xx, combined_dist(xx, values['alpha'], values['beta'], values['sigma_i'], full_fit=True),
                     label=f'{func} (α={values["alpha"]:.2f}, β={values["beta"]:.2f}, $sigma_i$={values["sigma_i"]:.2f} '
                           f'MSE={values["standard div"]:.2f})')
        if func == 'gamma full fit':
            ax.plot(
                xx,
                combined_dist_gamma(xx, values['alpha'], values['beta'], values['a'], values['b'], full_fit=True),
                label=f'{func} (α={values["alpha"]:.2f}, β={values["beta"]:.2f}, a={values["a"]:.2f}, b={values["b"]:.2f}'
                      f'MSE={values["standard div"]:.2f})'
            )
    plt.xlim(0, 1)
    plt.legend()
    if save:
        dir = "Plots/all"
        if not path.exists(dir):
            os.makedirs(dir)
        plt.savefig(f"{dir}/set{set}_{mode}_{num}.pdf")
    else:
        plt.show()
