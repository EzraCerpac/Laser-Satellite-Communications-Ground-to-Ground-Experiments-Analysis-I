import numpy as np
from matplotlib import pyplot as plt

from combined_fit.angular_jitter_fit_beta import estimate_sigma
from conf.data import Data


class Run:
    def __init__(self, data: Data, *args, **kwargs):
        self.data = data
        self.results = {}

    def calc_sigma(self, res: int = 1001, usable: float = 0.4, plot: bool = False):
        result = estimate_sigma(
            np.array(self.data.df), self.data.w_0, res, usable, plot
        )
        self.results['sigma'] = result
        if plot:
            plt.title(f'Histograms and Probs of {self.data}')
            plt.xlabel(r'$I_{norm}$')
            plt.ylabel(r'$p(I)$')
            plt.legend()
            plt.show()
        return self.results


class BatchRun:
    def __init__(self, data_sets):
        self.data = [[[Data(data_set, mode, number) for number in Data.mode_dict[mode]]
                      for mode in Data.mode_dict.keys()] for data_set in data_sets]
        self.results: dict[int, dict[bool, dict[int, dict[str, float]]]] = {}

    def run(self, *functions: str, **kwargs):
        print('Running Programs: ' + ' '.join([function for function in functions]))
        for i, data_set in enumerate(self.data):
            print(f'Running experiment {i + 1} of {len(self.data)}')
            mode_results = {}
            for j, data_mode in enumerate(data_set):
                number_results = {}
                for k, data in enumerate(data_mode):
                    print(f'\tRunning dataset {j * len(data_mode) + (k + 1)} of {len(data_mode) * len(data_set)}')
                    run = Run(data)
                    function_dict = {
                        'sigma': run.calc_sigma
                    }
                    try:
                        [function_dict[function](**kwargs) for function in functions]
                        number_results[data.number] = run.results
                    except RuntimeError:
                        print(f'RuntimeError in dataset {j * len(data_mode) + (k + 1)}')
                        plt.clf()
                mode_results[data_mode[0].mode] = number_results
            self.results[data_set[0][0].data_set] = mode_results
        return self.results
