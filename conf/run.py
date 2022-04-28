import multiprocessing as mp
import os
from os import path
from typing import Dict, List, Tuple, Any

import numpy as np
from matplotlib import pyplot as plt

from Model.inv_gamma import inv_gamma
from Model.main import estimate_sigma
from Model.main_without_scale import estimate_sigma as estimate_sigma_with_alpha
from Model.pure_lognormal import lognormal
from conf.data import Data
from info_plots.norm_I_hist import norm_I_hist
from misc.timing import timing

Result = Dict[int, Dict[bool, Dict[int, Dict[str, float]]]]


class Run:
    def __init__(self, data: Data):
        self.data = data
        self.results = {}
        fig, self.ax = plt.subplots()

    def _label(self, functions: List[str]):
        text = ''
        if 'lognormal' in functions:
            text += r'$skew_{lognormal}$: ' + str(round(self.results['lognormal skew'], 2)) + '\n'
            text += r'$pos_{lognormal}$: ' + str(format(self.results['lognormal pos'], '.2e')) + '\n'
        if 'inv gamma' in functions:
            text += r'$a_{inv gamma}$: ' + str(round(self.results['inv gamma a'], 2)) + '\n'
            text += r'$pos_{inv gamma}$: ' + str(format(self.results['inv gamma pos'], '.2e')) + '\n'
        if 'alpha' in self.results:
            text += r'$\alpha_{lognormal}$: ' + str(round(self.results['alpha'], 2)) + '\n'
        if 'beta' in self.results:
            text += r'$\beta_{lognormal}$: ' + str(round(self.results['beta'], 2)) + '\n'
        if 'alpha gamma' in self.results:
            text += r'$\alpha_{gamma}$: ' + str(round(self.results['alpha gamma'], 2)) + '\n'
        if 'beta gamma' in self.results:
            text += r'$\beta_{gamma}$: ' + str(round(self.results['beta gamma'], 2)) + '\n'
        text = text.strip('\n')

    def plot(self, functions: List[str], save: bool = False):
        norm_I_hist(np.array(self.data.df), bins=100)
        plt.title(f'Histograms and Probs of {self.data}')
        plt.xlabel(r'$I_{norm}$')
        plt.ylabel(r'$p(I)$')
        text = self._label(functions)
        props = dict(boxstyle='round', facecolor='white')
        plt.legend()
        self.ax.text(0.6, 0.7, text, fontsize=14, verticalalignment='top', transform=self.ax.transAxes, bbox=props)
        if save:
            dir = f"Plots/{'_'.join(functions)}"
            if not path.exists(dir):
                os.makedirs(dir)
            plt.savefig(f"{dir}/set{self.data.data_set}_{self.data.mode_rep}.pdf")
        else:
            plt.show()

    def calc_sigma(self, res: int = 101, plot: bool = False, **unused):
        result = estimate_sigma(np.array(self.data.df), self.data.w_0, False, res, plot)
        self.results['sigma'] = result[0]
        self.results['beta'] = result[1]
        self.results['standard div'] = result[-1]
        return self.results

    def calc_sigma_gamma(self, res: int = 101, plot: bool = False, **unused):
        result = estimate_sigma(np.array(self.data.df), self.data.w_0, True, res, plot)
        self.results['sigma gamma'] = result[0]
        self.results['beta gamma'] = result[1]
        self.results['standard div gamma'] = result[-1]
        return self.results

    def calc_sigma_with_alpha(self, res: int = 101, plot: bool = False, **unused):
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, False, res, plot)
        self.results['sigma'] = result[0]
        self.results['alpha'] = result[1]
        self.results['beta'] = result[2]
        self.results['standard div'] = result[-1]
        return self.results

    def calc_sigma_gamma_with_alpha(self, res: int = 101, plot: bool = False, **unused):
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, True, res, plot)
        self.results['sigma gamma'] = result[0]
        self.results['alpha gamma'] = result[1]
        self.results['beta gamma'] = result[2]
        self.results['standard div gamma'] = result[-1]
        return self.results

    def fit_lognormal(self, plot: bool = False, **unused):
        result = lognormal(np.array(self.data.df), plot)
        self.results['lognormal skew'] = result[0]
        self.results['lognormal pos'] = result[1]
        return self.results

    def fit_inv_gamma(self, plot: bool = False, **unused):
        result = inv_gamma(np.array(self.data.df), plot)
        self.results['inv gamma a'] = result[0]
        self.results['inv gamma pos'] = result[1]
        return self.results


class BatchRun:
    def __init__(self, data_sets):
        self.data = [[[Data(data_set, mode, number) for number in Data.mode_dict[mode]]
                      for mode in Data.mode_dict.keys()] for data_set in data_sets]
        self.results: Result = {}

    @timing
    def run(self, *functions: str, **kwargs) -> Result:
        """
        Run all functions on all data sets
        :param functions: functions to run
        :param kwargs:
            res: int, resolution of the histogram
            plot: bool, if True, plot the histogram
            save: bool, if True, save the plots
        :return: Result object (dict)
        """
        print('Running Programs: ' + ', '.join([function for function in functions]))
        for i, data_set in enumerate(self.data):
            print(f'Running experiment {i + 1} of {len(self.data)}')
            mode_results = {}
            for j, data_mode in enumerate(data_set):
                number_results = {}
                for k, data in enumerate(data_mode):
                    number_results[data.number] = \
                    self._run(data, data_mode, data_set, functions, j, k, kwargs, number_results)[1]
                mode_results[data_mode[0].mode] = number_results
            self.results[data_set[0][0].data_set] = mode_results
        return self.results

    @timing
    def run_parallel(self, *functions: str, **kwargs) -> List[Tuple[Any, Dict[Any, Any]]]:
        """
        Run all functions on all data sets in parallel
        :param functions: functions to run
        :param kwargs:
            res: int, resolution of the histogram
            plot: bool, if True, plot the histogram
            save: bool, if True, save the plots
        :return: Result object (dict)
        """
        pool = mp.Pool(mp.cpu_count())
        results = []
        print('Running Programs: ' + ', '.join([function for function in functions]))
        for i, data_set in enumerate(self.data):
            print(f'Running experiment {i + 1} of {len(self.data)}')
            for j, data_mode in enumerate(data_set):
                for k, data in enumerate(data_mode):
                    results.append(
                        pool.apply_async(self._run, args=(data, data_mode, data_set, functions, j, k, kwargs)))
        results = [result.get() for result in results]
        pool.close()
        print("\nDone!")
        return results

    @staticmethod
    def _run(data, data_mode, data_set, functions, j, k, kwargs) -> (Data, Result):
        print(f'\tRunning dataset {j * len(data_mode) + (k + 1)} of {len(data_mode) * len(data_set)}')
        run = Run(data)
        function_dict = {
            'sigma': run.calc_sigma,
            'sigma gamma': run.calc_sigma_gamma,
            'sigma_with_alpha': run.calc_sigma_with_alpha,
            'sigma_gamma_with_alpha': run.calc_sigma_gamma_with_alpha,
            'lognormal': run.fit_lognormal,
            'inv gamma': run.fit_inv_gamma,
        }
        try:
            [function_dict[function](**kwargs) for function in functions]
            if 'plot' in kwargs and kwargs['plot']:
                run.plot(functions, True if 'save' in kwargs and kwargs['save'] else False)
            return data, run.results
        except RuntimeError:
            print(f'RuntimeError in dataset {j * len(data_mode) + (k + 1)}')
            plt.clf()
