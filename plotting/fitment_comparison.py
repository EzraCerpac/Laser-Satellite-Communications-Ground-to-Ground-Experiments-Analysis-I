from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def comparison_plot(results: pd.DataFrame = pd.read_pickle('Results/results.pickle'), save: bool = False):
    fig, axs = plt.subplots(nrows=len(results), figsize=(5, 20))
    # fig.suptitle('Fitment MSE Comparison', fontsize=22)
    for i, set in enumerate(results):
        for j, datas in enumerate(results[set]):
            std_diffs = Counter()
            for num, fits in datas.items():
                for fit, vars in fits.items():
                    std_diffs[fit] += vars['standard div']

            axs[i * 2 + j].set_title(f'{set}urad, modes {"on" if j else "off"}', fontsize=16)
            labels, values = zip(*std_diffs.items())

            indexes = np.arange(len(labels))
            width = 0.7

            axs[i * 2 + j].bar(indexes, values, width)
            axs[i * 2 + j].set_xticks(indexes, labels)
    if save:
        plt.savefig('Plots/Fitment_Comparison.pdf')
    plt.show()
