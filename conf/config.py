import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from combined_fit.angular_jitter_fit_beta import estimate_sigma


class DataDF:
    def __init__(self, data_set: int, mode: bool, number: int):
        dir = {
            11: 'data11/'
        }
        mode_dict = {
            True: {
                'number': [2, 4, 8, 16, 28],
                'filename': f'{number} modes.pickle'
            },
            False: {
                'number': [1, 2, 3, 4, 5],
                'filename': f'off{number}.pickle'
            }
        }
        rootdir: str = 'Data/DFs/'
        self.file_path = rootdir + dir[data_set] + mode_dict[mode]['filename'] \
            if number in mode_dict[mode]['number'] else None
        self.df = pd.read_pickle(self.file_path)
        self.w_0 = data_set * 1e-6  # rad


class Run:
    def __init__(self, data: DataDF, *args, **kwargs):
        self.data = data
        self.results = []

    def calc_sigma(self, res: int = 1001, usable: float = 0.2, plot: bool = False):
        result = estimate_sigma(
            np.array(self.data.df), self.data.w_0, res, usable, plot
        )
        self.results.append(result)
        print(result)
        if plot:
            plt.legend()
            plt.show()
        return result


class FileConfig:
    def __init__(self):
        self.default_data: DataDF = DataDF(11, False, 1)
        self.data = self.default_data

    def data_set(self, data_set: int, mode: bool, number: int) -> DataDF:
        self.data = DataDF(data_set, mode, number)
        return self.data

    def run(self, *args, **kwargs) -> Run:
        return Run(self.data, *args, **kwargs)
