import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from combined_fit.angular_jitter_fit_beta import estimate_sigma


class DataDF:
    def __init__(self, data_set: int, mode: bool, number: int):
        assert data_set != 11, "Depreciated, use data18"
        self.data_set = data_set
        self.mode = mode
        self.number = number
        self.mode_rep = f'{number} modes' if mode else f'off{number}'

        dir = {
            11: 'data11/',
            18: 'data18/'
        }
        mode_dict = {
            True: {
                'number': [2, 4, 8, 16, 28],
            },
            False: {
                'number': [1, 2, 3, 4, 5],
            }
        }
        rootdir: str = 'Data/DFs/'
        self.file_path = rootdir + dir[data_set] + self.mode_rep + '.pickle' \
            if number in mode_dict[mode]['number'] else None
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
        print(result)
        if plot:
            plt.title(f'Histograms and Probs of {self.data}')
            plt.xlabel(r'$I_{norm}$')
            plt.ylabel(r'$p(I)$')
            plt.legend()
            plt.show()
        return result


class FileConfig:
    def __init__(self, default=False):
        self.data = DataDF() if default else None

    def data_set(self, data_set: int = 18, mode: bool = False, number: int = 2) -> DataDF:
        self.data = DataDF(data_set, mode, number)
        return self.data

    def run(self, *args, **kwargs) -> Run:
        return Run(self.data, *args, **kwargs)
