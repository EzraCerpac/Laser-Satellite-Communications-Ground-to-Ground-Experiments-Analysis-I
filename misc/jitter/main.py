from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import beta

from Data.data_test import import_data, split_data
from Data.tests_generated.beta_distibution import sample
from jitter.intensity_prob import IntensityDistribution
from jitter.random_pointing_angle import PointingProbability


def fit_all(dataset: dict) -> dict:
    beta_dict = {}
    I_norm = np.linspace(0, 1, 101)
    for mode, data in dataset.items():
        distribution = IntensityDistribution(data.irradiance)
        beta_dict[mode] = distribution.b
        plt.plot(I_norm, beta.pdf(I_norm, 1, beta_dict[mode]), label=mode)
    plt.legend()
    plt.show()
    return beta_dict


def main():
    data_folder = Path('../Data/CSV')
    data_dict = import_data(data_folder)
    df_dict = split_data(data_dict['data_11'])

    data = df_dict['28 modes']
    # data = sample

    # data18.plot()
    # plt.show()
    distribution = IntensityDistribution(data.irradiance, 16e-6)
    # distribution.plot()
    prob = PointingProbability(distribution.sigma)
    prob.plot()
    
    # fit_all(df_dict)


if __name__ == '__main__':
    main()
