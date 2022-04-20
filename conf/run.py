from typing import Dict

import numpy as np
from matplotlib import pyplot as plt

from Model.main import estimate_sigma
from Model.main_with_alpha import estimate_sigma as estimate_sigma_with_alpha
from conf.data import Data
from info_plots.norm_I_hist import norm_I_hist


class Run:
    def __init__(self, data: Data):
        self.data = data
        self.results = {}
        fig, self.ax = plt.subplots()

    def plot(self, save: bool = False):
        norm_I_hist(np.array(self.data.df), bins=100)
        plt.title(f'Histograms and Probs of {self.data}')
        plt.xlabel(r'$I_{norm}$')
        plt.ylabel(r'$p(I)$')
        text = ''
        if 'beta' in self.results:
            text += r'$\beta_{lognormal}$: ' + str(round(self.results['beta'], 2)) + '\n'
        if 'beta gamma' in self.results:
            text += r'$\beta_{gamma}$: ' + str(round(self.results['beta gamma'], 2)) + '\n'
        text = text.strip('\n')
        props = dict(boxstyle='round', facecolor='white')
        plt.legend()
        self.ax.text(0.6, 0.7, text, fontsize=14, verticalalignment='top', transform=self.ax.transAxes, bbox=props)
        if save:
            plt.savefig(f"Plots/fit_set{self.data.data_set}/{self.data.mode_rep}.pdf")
        else:
            plt.show()

    # def calc_sigma(self, res: int = 1001, usable: float = 0.4, plot: bool = False):
    #     """
    #     Old method for sigma estimation
    #     """
    #     result = estimate_sigma(
    #         np.array(self.data.df), self.data.w_0, res, usable, False
    #     )
    #     self.results['sigma'] = result[0]
    #     self.results['beta'] = result[1]
    #     self.results['standard div'] = result[-1]
    #     return self.results
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
        self.results['alpha'] = result[1]
        self.results['beta'] = result[2]
        self.results['standard div gamma'] = result[-1]
        return self.results


class BatchRun:
    def __init__(self, data_sets):
        self.data = [[[Data(data_set, mode, number) for number in Data.mode_dict[mode]]
                      for mode in Data.mode_dict.keys()] for data_set in data_sets]
        self.results: Dict[int, Dict[bool, Dict[int, Dict[str, float]]]] = {}

    def run(self, *functions: str, **kwargs):
        print('Running Programs: ' + ', '.join([function for function in functions]))
        for i, data_set in enumerate(self.data):
            print(f'Running experiment {i + 1} of {len(self.data)}')
            mode_results = {}
            for j, data_mode in enumerate(data_set):
                number_results = {}
                for k, data in enumerate(data_mode):
                    print(f'\tRunning dataset {j * len(data_mode) + (k + 1)} of {len(data_mode) * len(data_set)}')
                    run = Run(data)
                    function_dict = {
                        'sigma': run.calc_sigma,
                        'sigma gamma': run.calc_sigma_gamma,
                        'sigma_with_alpha': run.calc_sigma_with_alpha,
                        'sigma gamma_with_alpha': run.calc_sigma_gamma_with_alpha,
                    }
                    try:
                        [function_dict[function](**kwargs) for function in functions]
                        if 'plot' in kwargs and kwargs['plot']:
                            run.plot(True if 'save' in kwargs and kwargs['save'] else False)
                        number_results[data.number] = run.results
                    except RuntimeError:
                        print(f'RuntimeError in dataset {j * len(data_mode) + (k + 1)}')
                        plt.clf()
                mode_results[data_mode[0].mode] = number_results
            self.results[data_set[0][0].data_set] = mode_results
        return self.results
