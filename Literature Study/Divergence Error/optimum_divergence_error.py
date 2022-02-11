import numpy as np
from scipy.special import erfc
import matplotlib.pyplot as plt

plot_dir = "../../Plots"
filename = "optimum_ratio.pdf"

a_coeff = {
    0: 2.05613,
    1: -1.33146,
    2: -1.92403e-1,
    3: -2.51125e-2,
    4: -2.02818e-3,
    5: -8.87644e-5,
    6: -1.60597e-6
}

average_BER = np.linspace(-12, -2, 101)  # 10log
optimum_ratio = sum([a_coeff[i] * average_BER ** i for i in a_coeff.keys()])

plt.plot(average_BER, optimum_ratio)
plt.xlabel(r'$\log_{10}(\overline{\mathrm{BER}})$')
plt.ylabel(r'$\left(w_{0} / \sigma\right)_{\mathrm{opt}}$')
# plt.show()
plt.savefig(f"{plot_dir}/{filename}")