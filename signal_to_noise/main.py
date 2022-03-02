from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from Data.data_test import import_data, split_data


def sum_squares(array: np.ndarray) -> float:
    squares = array ** 2
    return sum(squares)


def SNR(data: np.ndarray, db: bool = False) -> float:
    floor = min(data)
    print(floor)
    snr = sum_squares(data) / sum_squares(data - floor)
    return 10 * np.log10(snr) if db else snr


def main():
    data_folder = Path('../Data/CSV')
    data1, _ = import_data(data_folder)
    df_dict = split_data(data1)

    plt.plot(df_dict['8 modes']['time [s]'], df_dict['8 modes']['irradiance'])
    plt.show()
    print(SNR(df_dict['8 modes']['irradiance']))


if __name__ == '__main__':
    main()
