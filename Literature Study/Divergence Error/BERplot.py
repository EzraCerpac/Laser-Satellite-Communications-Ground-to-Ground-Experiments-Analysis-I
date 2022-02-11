import numpy as np
from scipy.special import erfc
import matplotlib.pyplot as plt

plot_dir = "../../Plots"
filename = "BERplot.pdf"

Q = np.linspace(0, 8, 101)
BER = 0.5 * erfc(Q/np.sqrt(2))
plt.plot(Q, 10*np.log10(BER), label="no jitter")
plt.xlabel(r'$Q$ [-]')
plt.ylabel(r'BER [dB]')
plt.show()
# plt.savefig(f"{plot_dir}/{filename}")