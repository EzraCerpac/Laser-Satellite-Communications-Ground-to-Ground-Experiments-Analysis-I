import logging
import multiprocessing as mp
from typing import Dict

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import invgamma, lognorm

from Model.inv_gamma import inv_gamma, inv_gamma_curve_fit
from Model.pure_lognormal import lognormal, lognormal_curve_fit
from Model.with_beta import estimate_sigma as estimate_sigma_with_alpha
from conf import plotting
from conf.data import Data
from misc.timing import timing

log = logging.getLogger(__name__)

Result = Dict[int, Dict[bool, Dict[int, Dict[str, float]]]]


class Run:
    def __init__(self, data: Data):
        self.data = data
        self.results = {}
        fig, self.ax = plt.subplots(figsize=(8, 5))

    def fit_lognormal_in_beta(self, res: int = 101, plot: bool = False, **unused):
        self.results['lognormal in beta'] = {}
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, False, res, plot)
        self.results['lognormal in beta']['sigma'] = result[0]
        self.results['lognormal in beta']['alpha'] = result[1]
        self.results['lognormal in beta']['beta'] = result[2]
        self.results['lognormal in beta']['standard div'] = result[-1]
        return self.results

    def fit_gamma_in_beta(self, res: int = 101, plot: bool = False, **unused):
        self.results['gamma in beta'] = {}
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, True, res, plot)
        self.results['gamma in beta']['sigma'] = result[0]
        self.results['gamma in beta']['alpha'] = result[1]
        self.results['gamma in beta']['beta'] = result[2]
        self.results['gamma in beta']['standard div'] = result[-1]
        return self.results

    def fit_lognormal(self, plot: bool = False, **unused):
        self.results['lognormal'] = {}
        result1 = lognormal(np.array(self.data.df), plot=False)
        result2 = lognormal_curve_fit(np.array(self.data.df), plot=False)
        result = result1 if result1[-1] < result2[-1] else result2
        self.results['lognormal']['skew'] = result[0]
        self.results['lognormal']['pos'] = result[1]
        self.results['lognormal']['standard div'] = result[-1]
        if plot:
            plt.plot(xx := np.linspace(1e-5, 1, 1001), lognorm.pdf(xx, result[0], result[1]), label='lognormal fitment')
        return self.results

    def fit_inv_gamma(self, plot: bool = False, **unused):
        self.results['inv gamma'] = {}
        result1 = inv_gamma(np.array(self.data.df), plot=False)
        result2 = inv_gamma_curve_fit(np.array(self.data.df), plot=False)
        result = result1 if result1[-1] < result2[-1] else result2
        self.results['inv gamma']['a'] = result[0]
        self.results['inv gamma']['pos'] = result[1]
        self.results['inv gamma']['standard div'] = result[-1]
        if plot:
            plt.plot(xx := np.linspace(1e-5, 1, 1001), invgamma.pdf(xx, result[0], result[1]),
                     label='inverse gamma fitment')
        return self.results

    def calc_full_lognorm(self, res: int = 101, plot: bool = False, **unused):
        self.results['lognormal full fit'] = {}
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, False, res, plot, full_fit=True)
        self.results['lognormal full fit']['sigma'] = result[0]
        self.results['lognormal full fit']['alpha'] = result[1]
        self.results['lognormal full fit']['beta'] = result[2]
        self.results['lognormal full fit']['sigma_i'] = result[3]
        self.results['lognormal full fit']['standard div'] = result[-1]
        return self.results

    def calc_full_gamma_in_beta(self, res: int = 101, plot: bool = False, **unused):
        self.results['gamma full fit'] = {}
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, True, res, plot, full_fit=True)
        self.results['gamma full fit']['sigma'] = result[0]
        self.results['gamma full fit']['alpha'] = result[1]
        self.results['gamma full fit']['beta'] = result[2]
        self.results['gamma full fit']['a'] = result[3]
        self.results['gamma full fit']['b'] = result[4]
        self.results['gamma full fit']['standard div'] = result[-1]
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
    def run_parallel(self, *functions: str, **kwargs) -> Dict[int, Dict[bool, Dict[int, Dict[str, float]]]]:
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
        log.info(f'Running Programs on {mp.cpu_count()} processors: ' + ', '.join([function for function in functions]))
        results = []
        for i, data_set in enumerate(self.data):
            self.results[data_set[0][0].data_set] = {}
            for j, data_mode in enumerate(data_set):
                self.results[data_set[0][0].data_set][data_mode[0].mode] = {}
                for k, data in enumerate(data_mode):
                    self.results[data_set[0][0].data_set][data_mode[0].mode][data.number] = {}
                    results.append(
                        pool.apply_async(self._run, args=(data, functions, kwargs)))
        results = [result.get() for result in results]
        pool.close()
        for result in results:
            self.results[result[0].data_set][result[0].mode][result[0].number] = result[1]
        if 'results' in kwargs and kwargs['results']:
            pd.DataFrame.from_dict(self.results).to_pickle('Results/results.pickle')
        if 'plot' in kwargs and kwargs['plot']:
            plotting.plot_combined(self.results, save=True if 'save' in kwargs and kwargs['save'] else False)
        print("\nDone!")
        return self.results

    @staticmethod
    def _run(data, functions, kwargs) -> (Data, Result):
        run = Run(data)
        function_dict = {
            # 'sigma': run.calc_sigma,
            # 'sigma gamma': run.calc_sigma_gamma,
            'lognormal in beta': run.fit_lognormal_in_beta,
            'gamma in beta': run.fit_gamma_in_beta,
            'lognormal': run.fit_lognormal,
            'inv gamma': run.fit_inv_gamma,
            'lognormal full fit': run.calc_full_lognorm,
            'gamma full fit': run.calc_full_gamma_in_beta,
            #'sigma': run.calc_sigma,
            #'sigma gamma': run.calc_sigma_gamma,
            #'sigma_with_alpha': run.calc_sigma_with_alpha,
            #'sigma_gamma_with_alpha': run.calc_sigma_gamma_with_alpha,
        }
        [function_dict[function](**kwargs) for function in functions]
        log.info(f'Finished fitment of set{data.data_set} {data.mode} {data.number}')
        return data, run.results
