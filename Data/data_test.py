from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import os

starting_values_11 = {
    'off1': 31.8,
    '2 modes': 55.4,
    'off2': 96.9,
    '28 modes': 135.4,
    'off3': 180.2,
    '4 modes': 215.5,
    'off4': 258.0,
    '8 modes': 296.7,
    'off5': 343.6,
    '16 modes': 275.1
}


def import_data(directory: Path) -> dict[str, pd.DataFrame]:
    print(os.listdir(directory))
    paths = os.listdir(directory)
    return {path.strip('.csv'): pd.read_csv(directory / path, skiprows=1) for path in paths}


def split_data(data: pd.DataFrame, split_dict: dict[str, float] = starting_values_11) -> dict[str, pd.DataFrame]:
    timestep = .0004034
    length = 30
    df = {}
    for mode, start in split_dict.items():
        begin, end = int(start / timestep), int((start + length) / timestep)
        df[mode] = data.iloc[begin:end]
    return df


def norm_time(df):
    min_t = df.time.min()
    df.time = df.time - min_t
    return df


if __name__ == '__main__':
    folder = Path('CSV')
    # datasets = import_data(folder)
    # print(datasets)
    # data = split_data(data11, starting_values_11)

    data18 = pd.read_csv(folder / 'data18urad.csv', names=['sec', 'msec', 'irradiance'], skiprows=1)
    # data18.boxplot()

    plt.plot(data18.irradiance)
    plt.show()


