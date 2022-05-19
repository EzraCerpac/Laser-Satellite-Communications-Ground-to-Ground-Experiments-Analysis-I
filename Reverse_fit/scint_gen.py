import matplotlib.pyplot as plt
import numpy as np

from Reverse_fit.funcs import random_variable_generation, LPF


def Psci(*, psi, cut_off_freq, lpf_slope, sampling_freq, vector_length, mean_received_power):
    X1 = random_variable_generation(0, 1, int(vector_length * sampling_freq))
    X1_f = LPF(X1, cut_off_freq, lpf_slope, sampling_freq)
    X1_n = X1_f / np.sqrt(np.mean(X1 ** 2))
    P_sci = np.exp(mean_received_power + psi * X1_n)

    return P_sci


if __name__ == '__main__':
    P_sci = np.random.seed(0)
    Psci(
        psi=0.099725,
        cut_off_freq=0.9,
        lpf_slope=0.9,
        sampling_freq=80,
        vector_length=30,
        mean_received_power=1,
    )
    plt.hist(P_sci, bins=100, label='P_sci')
    plt.legend()
    plt.show()
