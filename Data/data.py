from pathlib import Path

import pandas as pd

starting_values = {
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


def import_data(directory: Path) -> list[pd.DataFrame]:
    path1 = 'data_11.csv'
    path2 = 'data_28.csv'
    d1 = pd.read_csv(directory / path1, names=['time [s]', 'irradiance'], skiprows=1)
    d2 = pd.read_csv(directory / path2, names=['time [s]', 'irradiance'], skiprows=1)
    return [d1, d2]


def split_data(data: pd.DataFrame, split_dict: dict[str, float] = starting_values) -> dict[str, pd.DataFrame]:
    timestep = .0004034
    length = 30
    df = {}
    for mode, start in split_dict.items():
        begin, end = int(start / timestep), int((start + length) / timestep)
        df[mode] = data.iloc[begin:end]
    return df


if __name__ == '__main__':
    folder = Path('CSV')
    data1, data2 = import_data(folder)
    data = split_data(data1, starting_values)
    print(data['off1'])
