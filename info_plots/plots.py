import matplotlib.pyplot as plt
import numpy as np


def sigmaplot(results):
    print(results)
    sigma_false = np.empty(0)
    sigma_true = np.empty(0)
    for i in range(1, 6):
        sigma_false = np.append(sigma_false, results[18][False][i]['sigma'])
    print(sigma_false)
    plt.plot()
