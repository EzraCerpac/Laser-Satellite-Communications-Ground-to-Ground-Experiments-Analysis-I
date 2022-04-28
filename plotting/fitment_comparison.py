from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def comparison_plot(results: pd.DataFrame = pd.read_pickle('Results/results.pickle'), save: bool = False):
    fig, axs = plt.subplots(*results.shape, figsize=(20, 20))
    for i, set in enumerate(results):
        for j, datas in enumerate(results[set]):
            std_diffs = Counter()
            for num, fits in datas.items():
                for fit, vars in fits.items():
                    try:
                        std_diffs[fit] += vars['standard div']
                    except KeyError:
                        pass

            axs[i, j].set_title(f'{set}urad, modes {"on" if j else "off"}')
            try:
                labels, values = zip(std_diffs.items())

                indexes = np.arange(len(labels))
                width = 1

                axs[i, j].bar(indexes, values, width)
                axs[i, j].xticks(indexes + width * 0.5, labels)
            except ValueError:
                pass
    plt.show()
