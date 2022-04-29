import multiprocessing as mp
import os
from os import path
from typing import Dict

import numpy as np
from matplotlib import pyplot as plt
from progress.bar import Bar
from scipy.stats import lognorm, invgamma

from Model.with_beta import combined_dist, combined_dist_gamma
from conf.config import Config
from plotting.norm_I_hist import norm_I_hist


def plot_combined(results: Dict[int, Dict[bool, Dict[int, Dict[str, Dict[str, float]]]]], save: bool = False) -> None:
    pool = mp.Pool(mp.cpu_count())
    plottings = []
    for set, modes in results.items():
        for mode, nums in modes.items():
            for num, funcs in nums.items():
                plottings.append(pool.apply_async(_plot_one, args=(funcs, mode, num, save, set)))
    [plot.get() for plot in plottings]
    pool.close()


def _plot_one(funcs, mode, num, save, set):
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.title(f'Histogram and Probs of {set}urad, mode {"on" if mode else "off"}: {num}')
    norm_I_hist(np.array(Config().set_data(set, mode, num).df), bins=300)
    xx = np.linspace(0, 1, 101)
    with Bar(f'Plotting set {set}, mode {"on" if mode else "off"}: {num}', max=len(funcs)) as bar:  # TODO: doesnot work
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
            bar.next()
    plt.legend()
    if save:
        dir = "Plots/all"
        if not path.exists(dir):
            os.makedirs(dir)
        plt.savefig(f"{dir}/set{set}_{mode}_{num}.pdf")
    else:
        plt.show()
