import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from combined_fit.angular_jitter_fit_beta import estimate_sigma


def main():
    data = pd.read_pickle('../Data/DFs/data11/off1.pickle')
    I = np.array(data)
    print(estimate_sigma(I, 11e-6, 301, 0.25, plot=True))
    plt.xlim(0, 0.5)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
