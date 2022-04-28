import matplotlib.pyplot as plt
import numpy as np


def sigmaplot(results):
    print(results)

    gemiddeldes = {}
    gemiddeldes[18] = {}
    gemiddeldes[22] = {}

    fig, (ax1, ax2) = plt.subplots(1, 2)

    for set in (18,):  # later (18, 22)
        gemiddeldes[set]['off'] = np.mean([results[set][False][i]['sigma'] for i in range(1, 6)])
        gemiddeldes[set]['on'] = np.mean([results[set][True][i]['sigma'] for i in [2,4,8,16,28]])

    for num in (18,):
        x1 = [1, 2, 3, 4, 5]
        y1 = [results[num][False][i]['sigma'] for i in range(1, 6)]
        my_xticks1 = ['1', '2', '3', '4', '5']
        plt.xticks(x1, my_xticks1)
        ax1.plot(x1, y1, '-ok', label='Set ' + str(num))
        ax1.set(xlabel='Datasets with modes off', ylabel='Sigma')
        #ax1.set_title('Sigma for datasets with modes off')
        ax1.grid(which='major', linewidth='0.9')
        ax1.legend()

        x2 = [1, 2, 3, 4, 5]
        y2 = [results[num][True][i]['sigma'] for i in [2,4,8,16,28]]
        my_xticks2 = ['2', '4', '8', '16', '28']
        plt.xticks(x2, my_xticks2)
        ax2.plot(x2, y2, '-ok', label='Set ' + str(num))
        ax2.set(xlabel='Number of modes in different datasets', ylabel='Sigma')
        #ax2.set_title('Sigma for datasets with modes on')
        ax2.grid(which='major', linewidth='0.9')
        ax2.legend()
    fig.suptitle('Sigma for datasets with modes off (left) and on (right)')
    plt.show()

    # plt.grid(which='major')
    #.clf()
