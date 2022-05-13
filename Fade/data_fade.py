import numpy as np
from matplotlib import pyplot as plt


def plot_fade_prob(irradiance: np.array, res: int = 101, plot: bool = True):
    irradiance_db = 10 * np.log10((np.mean(irradiance)) / irradiance)

    data_count = np.size(irradiance_db)
    xx = np.linspace(min(irradiance_db), max(irradiance_db), res)
    yy = np.zeros(0)

    for power_level in xx:
        yy = np.append(yy, np.size(np.where(irradiance_db < power_level)) / data_count)

    if plot:
        plt.plot(xx, yy, label="fade percent")

    return xx, yy, min(irradiance_db), max(irradiance_db)


def plot_fade_count(irradiance: np.array, res: int = 101, plot: bool = True):
    irradiance_db = 10 * np.log10((np.mean(irradiance)) / irradiance)

    time_length = 30
    xx = np.linspace(min(irradiance_db), max(irradiance_db), res)
    yy = np.zeros(0)

    for power_level in xx:
        yy = np.append(yy, np.size(np.where(irradiance_db < power_level)) / time_length)

    if plot:
        plt.plot(xx, yy, label="fade count")

    return xx, yy, min(irradiance_db), max(irradiance_db)


def plot_mean_time(irradiance: np.array, res: int = 101, plot: bool = True):
    result1 = plot_fade_prob(irradiance, res, plot)
    result2 = plot_fade_count(irradiance, res, plot)

    irradiance_db = 10 * np.log10((np.mean(irradiance)) / irradiance)
    xx = np.linspace(min(irradiance_db), max(irradiance_db), res)

    yy = result1[1] / result2[1]

    if plot:
        plt.plot(xx, yy, label="mean fade time")

    return xx, yy, min(irradiance_db), max(irradiance_db)
