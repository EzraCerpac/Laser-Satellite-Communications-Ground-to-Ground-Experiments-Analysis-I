import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from combined_fit.angular_jitter_fit_beta import estimate_sigma


class DataDF:
    dir = {
        11: 'data11/',
        18: 'data18/'
    }
    mode_dict = {
        False: [1, 2, 3, 4, 5],
        True: [2, 4, 8, 16, 28]
    }

    def __init__(self, data_set: int, mode: bool, number: int):
        assert data_set != 11, "Depreciated, use data18"
        self.data_set = data_set
        self.mode = mode
        self.number = number
        self.mode_rep = f'{number} modes' if mode else f'off{number}'

        rootdir: str = 'Data/DFs/'
        self.file_path = rootdir + DataDF.dir[data_set] + self.mode_rep + '.pickle' \
            if number in DataDF.mode_dict[mode] else None
        self.df = pd.read_pickle(self.file_path)
        self.w_0 = data_set * 1e-6  # rad

    def __repr__(self):
        return f'the {self.data_set}urad data set with {self.number if self.mode else "no"} modes'


class Run:
    def __init__(self, data: DataDF, *args, **kwargs):
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
        self.data = [[[DataDF(data_set, mode, number) for number in DataDF.mode_dict[mode]]
                      for mode in DataDF.mode_dict.keys()] for data_set in data_sets]
        self.results: dict[int, dict[bool, dict[int, dict[str, float]]]] = {}

    def run(self, *functions: str):
        print('Running Programs: ' + ' '.join([function for function in functions]))
        for i, data_set in enumerate(self.data):
            print(f'Running experiment {i + 1} of {len(self.data)}')
            mode_results = {}
            for j, data_mode in enumerate(data_set):
                number_results = {}
                for k, data in enumerate(data_mode):
                    print(f'\tRunning dataset {(j) * len(data_mode) + (k + 1)} of {len(data_mode) * len(data_set)}')
                    run = Run(data)
                    function_dict = {
                        'sigma': run.calc_sigma
                    }
                    do = [function_dict[function]() for function in functions]
                    number_results[data.number] = run.results
                mode_results[data_mode[0].mode] = number_results
            self.results[data_set[0][0].data_set] = mode_results
        return self.results


class FileConfig:
    def __init__(self, default=False):
        if default:
            self.set_data()
        else:
            self.data = None

    def set_data(self, data_set: int = 18, mode: bool = False, number: int = 2) -> DataDF:
        self.data = DataDF(data_set, mode, number)
        return self.data

    def run(self, *args, **kwargs) -> Run:
        return Run(self.data, *args, **kwargs)

    def run_batch(self, data_sets):
        return BatchRun(data_sets)
