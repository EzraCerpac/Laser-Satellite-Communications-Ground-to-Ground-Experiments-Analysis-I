import pandas as pd


class Data:
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
        self.file_path = rootdir + Data.dir[data_set] + self.mode_rep + '.pickle' \
            if number in Data.mode_dict[mode] else None
        self.df = pd.read_pickle(self.file_path)
        self.w_0 = data_set * 1e-6  # rad

    def __repr__(self):
        return f'the {self.data_set}urad data set with {self.number if self.mode else "no"} modes'
