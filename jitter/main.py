from pathlib import Path

from matplotlib import pyplot as plt

from Data.data import import_data
from jitter.intensity_prob import IntensityDistribution


def main():
    data_folder = Path('../Data/CSV')
    data1, _ = import_data(data_folder)
    # data1.plot()
    # plt.show()
    distribution = IntensityDistribution(data1.intensity)
    distribution.plot()
    # print(distribution.sigma)


if __name__ == '__main__':
    main()
