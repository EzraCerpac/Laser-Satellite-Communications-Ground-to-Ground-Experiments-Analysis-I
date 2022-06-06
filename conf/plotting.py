import logging
import multiprocessing as mp
import os
import time
from os import path
from typing import Dict, Optional

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import lognorm, invgamma, beta

from Model.lognormal_paper_based import lognormal_paper, lognormal_paper_true
from Model.pure_combined import func as comb_func
from Model.pure_combined import func_paper as comb_func_paper
from Model.pure_combined import func_paper_gamma as comb_func_paper_gamma
from Model.pure_gamma_gamma import gamma_gamma_paper
from Model.with_beta import combined_dist, combined_dist_gamma
from conf.data import Data
from plotting.norm_I_hist import norm_I_hist

log = logging.getLogger(__name__)

LW = 2

name_convert = {
    'lognormal in beta': 'lib',
    'gamma in beta': 'gib',
    'beta': 'beta',
    'lognormal': 'ln',
    'combined': 'combined',
    'inv gamma': 'ig',
    'gamma full fit': 'gff',
    'lognormal full fit': 'lff',
    'lognormal paper': 'lognormal',
    'lognormal paper true': 'lognormal',
    'gamma gamma paper': 'gamma gamma',
    'combined paper': 'combined lognormal',
    'combined paper gamma': 'combined gamma gamma',
}


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



def _plot_one(funcs: dict, mode: Optional[bool] = None, num: Optional[int] = None, set: Optional[int] = None,
              save: bool = False, dir: str = time.strftime("%d-%m-%Y_%H-%M"),
              data: Optional[np.ndarray] = None) -> None:
    linestyles = ['o-', 'D-', '^-', 's-', '*-', 'P-']
    try:
        fig, ax = plt.subplots(figsize=(7, 5))
        # plt.title(f'Histogram and Probs of {set}urad, mode {"on" if mode else "off"}: {num}')
        plt.xlabel(r'$I_{norm}$')
        plt.ylabel(r'PDF')
        if mode is not None:
            norm_I_hist(np.array(Data(set, mode, num).df), bins=300)
        elif data is not None:
            # log.info(f"data is type: {type(data)}")
            norm_I_hist(data, bins=300)
        xx = np.linspace(1e-10, 1, 601)
        # log.info(f'Plotting set {set}, modes {"on" if mode else "off"}, {num}')
        for func, values in funcs.items():
            plt.xlim(0, 1)
            if func == 'lognormal in beta':
                ax.plot(
                    xx,
                    combined_dist(xx, values['alpha'], values['beta']), linestyles.pop(), markevery=14,
                    label=f'{name_convert[func]} (α={values["alpha"]:.3g}, β={values["beta"]:.3g})'
                    # linewidth=LW
                )
            if func == 'gamma in beta':
                ax.plot(
                    xx,
                    combined_dist_gamma(xx, values['alpha'], values['beta']), linestyles.pop(), markevery=14,
                    label=f'{name_convert[func]} (α={values["alpha"]:.3g}, β={values["beta"]:.3g})'
                    # linewidth=LW
                )
            if func == 'beta':
                plt.plot(
                    xx,
                    beta.pdf(xx, values['a'], values['b']), linestyles.pop(), markevery=14,
                    label=f'{name_convert[func]} (β={values["a"]:.3g})'
                    # linewidth=LW
                )
            if func == 'lognormal':
                plt.plot(
                    xx,
                    lognorm.pdf(xx, values['skew'], values['pos']), linestyles.pop(), markevery=14,
                    label=f'{name_convert[func]}''\n'f'(σ={values["skew"]:.3g}, μ={values["pos"]:.3g})'
                    # linewidth=LW
                )
            if func == 'lognormal paper':
                plt.plot(
                    xx,
                    lognormal_paper(xx, values['sigma_i'], values['mu'], values['I_0']), linestyles.pop(), markevery=14,
                    label=f'{name_convert[func]}''\n' f'($\sigma_i^2$={values["sigma_i"]:.3g}, $\mu$={values["mu"]:.3g})'
                    # linewidth=LW
                )
            if func == 'lognormal paper true':
                plt.plot(
                    xx,
                    lognormal_paper_true(xx, values['sigma_i'], values['I_0']), linestyles.pop(), markevery=14,
                    # label=f'{name_convert[func]}''\n' f'($\sigma_i^2$={values["sigma_i"]:.3g}, $\mu^*$={-0.5 * (values["sigma_i"]):.3g}, I0 = {values["I_0"]:.3g})'
                    label=f'{name_convert[func]}''\n' f'($\sigma_i^2$={values["sigma_i"]:.3g}, $I_0$ = {values["I_0"]:.3g})'
                    # linewidth=LW
                )

            if func == 'gamma gamma paper':
                plt.plot(
                    xx,
                    gamma_gamma_paper(xx, values['sigma_r'], values['I_0']), linestyles.pop(), markevery=14,
                    # label=f'{name_convert[func]}''\n' f'($\sigma_i^2$={values["sigma_i"]:.3g}, $\mu^*$={-0.5 * (values["sigma_i"]):.3g}, I0 = {values["I_0"]:.3g})'
                    label=f'{name_convert[func]}''\n' f'($\sigma_r^2$={values["sigma_r"]:.3g}, $I_0$ = {values["I_0"]:.3g})'
                    # linewidth=LW
                )

            if func == 'combined':
                plt.plot(
                    xx,
                    comb_func(xx, values['a'], values['b'], values['c']), linestyles.pop(), markevery=14,
                    label=f'{name_convert[func]}''\n'f'($\sigma_i^2$={values["b"]:.3g}, μ={values["c"]:.3g}, β={values["a"]:.3g})'
                    # linewidth=LW
                )

            if func == 'combined paper':
                plt.plot(
                    xx,
                    comb_func_paper(xx, values['sigma_i2'], values['beta_b'], values['I_0']), linestyles.pop(), markevery=14,
                    label=f'{name_convert[func]}' '\n' f'($\sigma_i^2$={values["sigma_i2"]:.3g}, β={values["beta_b"]:.3g})'
                    # linewidth=LW
                )

            if func == 'combined paper gamma':
                plt.plot(
                    xx,
                    comb_func_paper_gamma(xx, values['sigma_r2'], values['beta_b'], values['I_0']), linestyles.pop(), markevery=14,
                    label=f'{name_convert[func]}' '\n' f'($\sigma_r^2$={values["sigma_r2"]:.3g}, β={values["beta_b"]:.3g})'
                    # linewidth=LW
                )


            if func == 'inv gamma':
                plt.plot(
                    xx,
                    invgamma.pdf(xx, values['a'], values['pos']), linestyles.pop(), markevery=14,
                    label=f'{name_convert[func]} (α={values["a"]:.3g}, β={values["pos"]:.3g})'
                    # linewidth=LW
                )
            if func == 'lognormal full fit':
                plt.plot(xx, combined_dist(xx, values['alpha'], values['beta'], values['sigma_i'], full_fit=True),
                         linestyles.pop(), markevery=7,
                         label=f'{name_convert[func]} (α={values["alpha"]:.3g}, β={values["beta"]:.3g}, $\sigma_i$={values["sigma_i"]:.3g})'
                         # linewidth=LW
                         )
            if func == 'gamma full fit':
                ax.plot(
                    xx,
                    combined_dist_gamma(xx, values['alpha'], values['beta'], values['a'], values['b'], full_fit=True),
                    linestyles.pop(), markevery=14,
                    label=f'{name_convert[func]} (α={values["alpha"]:.3g}, β={values["beta"]:.3g},'
                          '\n'
                          f'        a={values["a"]:.3g}, b={values["b"]:.3g})'
                    # linewidth=LW
                )

            if func == 'fade probability data':
                plt.plot(
                    values['F_t'], values['Prob'],
                    label=f'{name_convert[func]}'
                )
                plt.xlim(values['Min'], values['Max'])
                plt.yscale("log")

            if func == 'fade count data':
                plt.plot(
                    values['F_t'], values['Time'],
                    label=f'{name_convert[func]}'
                )
                plt.xlim(values['Min'], values['Max'])
                plt.yscale("log")
            if func == 'fade mean time data':
                plt.plot(
                    values['F_t'], values['Time'],
                    label=f'{name_convert[func]}'
                )
                plt.xlim(values['Min'], values['Max'])
                plt.yscale("log")

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
        log.error(f'Failed to plot set{set} {mode} {num}: {e}', exc_info=True)
