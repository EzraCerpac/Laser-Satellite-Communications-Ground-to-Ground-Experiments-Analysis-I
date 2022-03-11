import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_pickle('../Data/DFs/data11/off1.pickle')

x = np.arange(0, len(data))

plt.plot(x, data)
plt.show()


