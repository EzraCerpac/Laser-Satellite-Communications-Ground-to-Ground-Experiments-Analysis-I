from pathlib import Path

import pandas as pd


def import_data(directory: Path):
    path1 = 'data_11.csv'
    path2 = 'data_28.csv'
    data1 = pd.read_csv(directory / path1, names=['time [s]', 'intensity'], index_col=0, skiprows=1)
    data2 = pd.read_csv(directory / path2, names=['time [s]', 'intensity'], index_col=0, skiprows=1)
    return data1, data2


if __name__ == '__main__':
    folder = Path('CSV')
    data1, data2 = import_data(folder)
    print(data1.head())
