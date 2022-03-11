from pathlib import Path
import pandas as pd
import pickle

from matplotlib import pyplot as plt

starting_values_18 = {
    'off1': 46.3,
    '2 modes': 100.0,
    'off2': 172.3,
    '28 modes': 240.3,
    'off3': 318.1,
    '4 modes': 382.0,
    'off4': 472.9,
    '8 modes': 527.6,
    'off5': 603.3,
    '16 modes': 675.2
}


def split_data(data: pd.DataFrame, split_dict: dict[str, float] = starting_values_11) -> pd.DataFrame:
    timestep = .0004034
    length = 30
    df_dict = {}
    for mode, start in split_dict.items():
        begin, end = int(start / timestep), int((start + length) / timestep)
        df_dict[mode] = data.iloc[begin:end].irradiance
    df = pd.concat(df_dict)
    return df


if __name__ == '__main__':
    folder = Path('CSV')

    data11 = pd.read_csv(folder / 'data_11.csv', names=['time', 'irradiance'], skiprows=1)
    data11 = split_data(data11)
    data22 = pd.read_csv(folder / 'data22urad.csv', names=['index', 'time', 'irradiance'], skiprows=1)
    Cn_df = pd.read_csv(folder / 'Cnprofile.csv')

    pickle_dir = Path('DFs')
    # for mode in starting_values_11.keys():
    #     print(mode)
    #     with open(pickle_dir / f"data11/{mode}.pickle", 'wb') as f:
    #         pickle.dump(data11[mode], f)

    plt.plot(data22.time, data22.irradiance)
    plt.show()

    # with open(pickle_dir / f"data18.pickle", 'wb') as f:
    #     pickle.dump(Cn_df, f)
    
    
else:
    folder = Path('../Data/CSV')
