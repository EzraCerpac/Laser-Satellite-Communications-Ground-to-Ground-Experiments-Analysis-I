import numpy as np
from scipy.integrate import quad
from scipy.special import erfc
import matplotlib.pyplot as plt

plot_dir = "../../Plots"
filename = "BER_w_sigma.pdf"

Q = np.linspace(0.01, 8, 101)
BER = 0.5 * erfc(Q / np.sqrt(2))
ber_dict = {
    5: [],
    10: [],
    20: [],
    40: []
}


def average_BER(Q, w_sigma):
    beta = w_sigma ** 2 / 4
    integral = quad(lambda I: I ** (beta - 1) * erfc(I * Q * (beta + 1) / (np.sqrt(2) * beta)), 0, 1)
    return (Q * (beta + 1)) / 2 * integral[0]

for w_sigma in ber_dict.keys():
    bers = []
    for q in Q:
        bers.append(average_BER(q, w_sigma))
    ber_dict[w_sigma] = bers

plt.plot(Q, 10 * np.log10(BER), label="no jitter")
for w_sigma, ber in ber_dict.items():
    plt.plot(Q, 10 * np.log10(ber), label=r"$w_0/\sigma=$"+str(w_sigma))
plt.xlabel(r'$Q$ [-]')
plt.ylabel(r'BER [dB]')
plt.legend(loc="best")
# plt.show()
plt.savefig(f"{plot_dir}/{filename}")
