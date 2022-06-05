from __future__ import annotations

import multiprocessing as mp
import time
from typing import Dict

import pandas as pd

from conf import plotting
from conf.data import Data
from conf.run import Result, log, Run
from misc.timing import timing


class BatchRun:
    def __init__(self, data_sets):
        self.data = [[[Data(data_set, mode, number) for number in Data.mode_dict[mode]]
                      for mode in Data.mode_dict.keys()] for data_set in data_sets]
        self.results: Result = {}

    @timing
    def run_single(self, data, *functions, **kwargs):
        self.results = self._run_parallel(data, functions, kwargs)[1]
        if kwargs.get('plot', False):
            # plt.hist(data.df, bins=100, density=True, label='P_comb')
            plotting._plot_one(
                self.results,
                data=data.df,
                save=True if 'save' in kwargs and kwargs['save'] else False,
                dir=f'Plots/{time.strftime("%d-%m-%Y-%H-%M")}')
        print("\nDone!")
        return self.results

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
                    number_results[data.number] = self._run(data, functions, kwargs)[1]
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
        functions_22 = [function for function in functions if
                        function != 'lognormal full fit' and function != 'gamma full fit']
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
                        pool.apply_async(self._run, args=(data, functions if i == 0 else functions_22, kwargs)))
        results = [result.get() for result in results]
        pool.close()
        for result in results:
            self.results[result[0].data_set][result[0].mode][result[0].number] = result[1]
        if 'results' in kwargs and kwargs['results']:
            pd.DataFrame.from_dict(self.results).to_pickle(f'Results/{time.strftime("%d-%m-%Y")}.pickle')
        if 'plot' in kwargs and kwargs['plot']:
            plotting.plot_combined(self.results, save=True if kwargs.get('save') else False)
        print("\nDone!")
        return self.results

    @staticmethod
    def _run(data: Data, functions, kwargs) -> (Data, Result):
        run = Run(data)
        function_dict = {
            'lognormal in beta': run.fit_lognormal_in_beta,
            'gamma in beta': run.fit_gamma_in_beta,
            'beta': run.fit_beta,
            'lognormal': run.fit_lognormal,
            'lognormal paper': run.fit_lognormal_paper,
            'gamma gamma paper': run.fit_gamma_gamma_paper,
            'lognormal paper true': run.fit_lognormal_paper_true,
            'combined': run.fit_combined,
            'combined paper': run.fit_combined_paper,
            'combined paper gamma': run.fit_combined_paper_gamma,
            'inv gamma': run.fit_inv_gamma,
            'lognormal full fit': run.calc_full_lognorm,
            'gamma full fit': run.calc_full_gamma_in_beta,
            'fade probability data': run.fade_prob_data,
            'fade count data': run.fade_count_data,
            'fade mean time data': run.fade_mean_data,
        }
        try:
            [function_dict[function](**kwargs) for function in functions]
            log.info(f'Finished fitment of set{data.data_set} {data.mode} {data.number}')
        except Exception as e:
            log.error(f'Failed to fit set{data.data_set} {data.mode} {data.number}: {e}')
        return data, run.results

    @staticmethod
    def _run_parallel(data: Data, functions, kwargs) -> (Data, Result):
        log.info(f'Running Programs on {mp.cpu_count()} processors: ' + ', '.join([function for function in functions]))
        run = Run(data)
        function_dict = {
            'lognormal in beta': run.fit_lognormal_in_beta,
            'gamma in beta': run.fit_gamma_in_beta,
            'beta': run.fit_beta,
            'lognormal': run.fit_lognormal,
            'lognormal paper': run.fit_lognormal_paper,
            'lognormal paper true': run.fit_lognormal_paper_true,
            'gamma gamma paper': run.fit_gamma_gamma_paper,
            'combined': run.fit_combined,
            'combined paper': run.fit_combined_paper,
            'combined paper gamma': run.fit_combined_paper_gamma,
            'inv gamma': run.fit_inv_gamma,
            'lognormal full fit': run.calc_full_lognorm,
            'gamma full fit': run.calc_full_gamma_in_beta,
            'fade probability data': run.fade_prob_data,
            'fade count data': run.fade_count_data,
            'fade mean time data': run.fade_mean_data,
        }
        pool = mp.Pool(mp.cpu_count())
        results = []
        for function in functions:
            results.append(pool.apply_async(function_dict[function], kwds=kwargs))
        results_lst = [result.get() for result in results]
        results = {list(result.keys())[0]: list(result.values())[0] for result in results_lst}
        pool.close()
        # except Exception as e:
        #     log.error(f'Failed to fit set{data.data_set} {data.mode} {data.number}: {e}')
        return data, results
