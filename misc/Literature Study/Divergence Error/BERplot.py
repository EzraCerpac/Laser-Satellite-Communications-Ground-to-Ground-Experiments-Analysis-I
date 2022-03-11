import matplotlib.pyplot as plt

from misc.formula.ber_from_w_sigma import *

# plt.rcParams['axes.prop_cycle'] = ("cycler('color', list('rbgk')) +"
#                                    "cycler('linestyle', ['-', '--', ':', '-.'])")

plot_dir = "../../../Plots"
filename = "BER_w_sigma.pdf"

Q = np.linspace(0.01, 8, 101)
ber_dict = {
    5: [],
    10: [],
    25: [],
    100: []
}

for w_sigma in ber_dict.keys():
    bers = []
    for q in Q:
        bers.append(average_BER(q, w_sigma))
    ber_dict[w_sigma] = bers

plt.plot(Q, 10 * np.log10(BER(Q)), label="no jitter")
for w_sigma, ber in ber_dict.items():
    plt.plot(Q, 10 * np.log10(ber), label=r"$w_0/\sigma=$" + str(w_sigma))
plt.xlabel(r'$Q$ [-]')
plt.ylabel(r'BER [dB]')
plt.legend(loc="best")
plt.show()
# plt.savefig(f"{plot_dir}/{filename}")
