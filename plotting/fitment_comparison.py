import logging
import os
import time
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def comparison_plot(results_file: str = 'Results/results.pickle', save: bool = False):
    log.info('Making comparison plot')
    results = pd.read_pickle(results_file)
    # fig.suptitle('Fitment MSE Comparison', fontsize=22)
    for i, set in enumerate(results):
        if i == 0:
            for j, datas in enumerate(results[set]):
                fig, axs = plt.subplots(figsize=(5, 4))
                try:
                    std_diffs = Counter()
                    for num, fits in datas.items():
                        for fit, vars in fits.items():
                            try:
                                # if fit != 'gamma full fit':
                                std_diffs[fit] += vars['standard div']
                            except KeyError:
                                log.warning(f'MSE not found in {fit}')

                    # axs.set_title(f'{set}urad, modes {"on" if j else "off"}', fontsize=16)
                    labels, values = zip(*std_diffs.items())

                    indexes = np.arange(len(labels))
                    width = 0.7

                    axs.bar(indexes, values, width)
                    new_labels = []
                    for label in labels:
                        new_labels.append(label.replace(' ', '\n', 1))

                    axs.set_xticks(indexes, new_labels)
                    axs.set_ylabel('Mean Squared Error')
                    # axs[i * 2 + j].set_ylim(0, std_diffs.most_common()[1][1] * 1.3)
                    # highest = std_diffs.most_common(1)[0]
                    # if highest[1] > axs[i * 2 + j].get_ylim()[1]:
                    #     axs[i * 2 + j].text((labels.index(highest[0]) + .5) / len(labels), 0.9, f'{highest[1]:.2g}',
                    #                         size=11, ha='center', va='center', transform=axs[i * 2 + j].transAxes)
                    fig.tight_layout()
                    if save:
                        dir = f'Plots/{time.strftime("%d-%m-%Y_%H:%M")}Fitment_Comparison'
                        if not os.path.exists(dir):
                            os.makedirs(dir)
                        path = f'{dir}/{set}urad_modes_{"on" if j else "off"}.pdf'
                        plt.savefig(path)
                        log.info(f'Saved comparison plot to: {path}')
                except Exception as e:
                    log.error(f'Error plotting {set} {"on" if j else "off"}: {e}')

    plt.show()
