import multiprocessing as mp
import warnings

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import IntegrationWarning

from Model.main_without_scale import combined_dist

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=IntegrationWarning)


def calc_and_plot(x, a, b) -> ((float, float), list[float]):
    return (a, b), combined_dist(x, a, b)


def main():
    pool = mp.Pool(processes=mp.cpu_count())

    todo = []
    a_num = 4

    x = np.arange(0.0, 1.0, 0.01)
    fig = plt.figure(1, figsize=(16, 12))
    for a in np.linspace(5, 10, a_num):
        for b in np.linspace(0.1, 1, 6):
            todo.append(pool.apply_async(calc_and_plot, args=(x, a, b)))

    new_as = []
    ax = fig.add_subplot(111)
    for (a, b), y in [p.get() for p in todo]:
        if a not in new_as:
            new_as.append(a)
            ax.legend()
            ax = fig.add_subplot(2, 2, new_as.index(a) + 1)
        ax.plot(x, y, label="a={}, b={}".format(a, b))
    ax.legend()
    plt.show()


if __name__ == '__main__':
    main()
