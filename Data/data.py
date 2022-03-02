from pathlib import Path
import pandas as pd
import pickle

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
    # data18 = pd.read_csv(folder / 'data18urad.csv', names=['sec', 'msec', 'irradiance'], skiprows=1)
    Cn_df = pd.read_csv(folder / 'Cnprofile.csv')

    pickle_dir = Path('DFs')
    # for mode in starting_values_11.keys():
    #     print(mode)
    #     with open(pickle_dir / f"data11/{mode}.pickle", 'wb') as f:
    #         pickle.dump(data11[mode], f)

    with open(pickle_dir / f"Cn.pickle", 'wb') as f:
        pickle.dump(Cn_df, f)
    
    
else:
    folder = Path('../Data/CSV')
