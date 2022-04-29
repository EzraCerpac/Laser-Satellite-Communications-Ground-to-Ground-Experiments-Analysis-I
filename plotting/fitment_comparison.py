from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def comparison_plot(results: pd.DataFrame = pd.read_pickle('Results/results.pickle'), save: bool = False):
    fig, axs = plt.subplots(*results.shape, figsize=(10, 10))
    fig.suptitle('Fitment Comparison', fontsize=22)
    for i, set in enumerate(results):
        for j, datas in enumerate(results[set]):
            std_diffs = Counter()
            for num, fits in datas.items():
                for fit, vars in fits.items():
                    std_diffs[fit] += vars['standard div']

            axs[i, j].set_title(f'{set}urad, modes {"on" if j else "off"}', fontsize=16)
            labels, values = zip(*std_diffs.items())

            indexes = np.arange(len(labels))
            width = 0.7

            axs[i, j].bar(indexes, values, width)
            axs[i, j].set_xticks(indexes, labels, fontsize=8)

    plt.show()
