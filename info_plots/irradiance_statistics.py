from matplotlib import pyplot as plt

from Data.data import *

# for mode, set in data18:
#     info[mode] = {
#         'mean': set.irradiance.describe()['mean'],
#         'scintillation': set.irradiance.describe()['std']
#     }
#
# xx = list(range(len(info.keys()))) # the label locations
# width = 0.35  # the width of the bars
#
# fig, ax = plt.subplots()
# means = ax.bar([x - width/2 for x in xx], [value['mean'] for value in info.values()], width, label='mean')
# scintillations = ax.bar([x + width/2 for x in xx], [value['scintillation'] for value in info.values()], width, label='scintillation')
# ax.set_xticks(xx, [mode for mode in info.keys()])
# ax.legend()
# plt.show()


data18.plot()
plt.show()
