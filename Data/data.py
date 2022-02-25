from pathlib import Path

import matplotlib.pyplot as plt
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
    
    # data1.plot()
    # plt.show()
    
    info = {}
    for mode, set in data.items():
        info[mode] = {
            'mean': set.irradiance.describe()['mean'],
            'scintillation': set.irradiance.describe()['std']
        }

    xx = list(range(len(info.keys()))) # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    means = ax.bar([x - width/2 for x in xx], [value['mean'] for value in info.values()], width, label='mean')
    scintillations = ax.bar([x + width/2 for x in xx], [value['scintillation'] for value in info.values()], width, label='scintillation')
    ax.set_xticks(xx, [mode for mode in info.keys()])
    ax.legend()
    plt.show()
