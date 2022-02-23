from pathlib import Path

from matplotlib import pyplot as plt

from Data.data import import_data, split_data
from Data.tests_generated.beta_distibution import sample
from jitter.intensity_prob import IntensityDistribution


def main():
    data_folder = Path('../Data/CSV')
    data1, _ = import_data(data_folder)
    df_dict = split_data(data1)

    data = df_dict['off1']
    # data = sample

    # data1.plot()
    # plt.show()
    distribution = IntensityDistribution(data.irradiance)
    distribution.plot()
    print(distribution.sigma)


if __name__ == '__main__':
    main()
