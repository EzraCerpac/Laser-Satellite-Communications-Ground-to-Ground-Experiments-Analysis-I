import logging
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Data.timeframe import time

log = logging.getLogger(__name__)


def comparison_plot(results_file: str = 'Results/results.pickle', save: bool = False):
    results = pd.read_pickle(results_file)
    fig, axs = plt.subplots(nrows=4, figsize=(5, 20))
    # fig.suptitle('Fitment MSE Comparison', fontsize=22)
    for i, set in enumerate(results):
        for j, datas in enumerate(results[set]):
            try:
                std_diffs = Counter()
                for num, fits in datas.items():
                    for fit, vars in fits.items():
                        try:
                            if fit != 'gamma full fit':  # TODO: because it messes up the scaling
                                std_diffs[fit] += vars['standard div']
                        except KeyError:
                            log.warning(f'MSE not found in {fit}')

                axs[i * 2 + j].set_title(f'{set}urad, modes {"on" if j else "off"}', fontsize=16)
                labels, values = zip(*std_diffs.items())

                indexes = np.arange(len(labels))
                width = 0.7

                axs[i * 2 + j].bar(indexes, values, width)
                axs[i * 2 + j].set_xticks(indexes, labels, rotation=45)
            except Exception as e:
                log.error(f'Error plotting {set} {"on" if j else "off"}: {e}')
    if save:
        plt.savefig(f'Plots/{time.strftime("%d-%m-%Y_%H:%M")}Fitment_Comparison.pdf')
    plt.show()
