import matplotlib.pyplot as plt
import numpy as np

from Reverse_fit.funcs import random_variable_generation, LPF


def Pjit(*, beam_divergence, pointing_jitter, cut_off_freq, lpf_slope, sampling_freq, vector_length):
    X1 = random_variable_generation(0, 1, int(vector_length * sampling_freq))
    X1_f = LPF(X1, cut_off_freq, lpf_slope, sampling_freq)
    X1_n = X1_f / np.sqrt(np.mean(X1 ** 2))

    X2 = random_variable_generation(0, 1, int(vector_length * sampling_freq))
    X2_f = LPF(X2, cut_off_freq, lpf_slope, sampling_freq)
    X2_n = X2_f / np.sqrt(np.mean(X2 ** 2))

    sigma = np.sqrt(2 / (4 - np.pi) * pointing_jitter)
    BW = sigma * np.sqrt(X1_n ** 2 + X2_n ** 2)

    P_jit = np.exp(BW ** 2 / beam_divergence)

    return P_jit


if __name__ == '__main__':
    np.random.seed(0)
    P_jit = Pjit(
        beam_divergence=18e-9,
        pointing_jitter=1e-9,
        cut_off_freq=0.9,
        lpf_slope=80,
        sampling_freq=10,
        vector_length=30,
    )
    plt.hist(P_jit, bins=100, label='P_jit')
    plt.legend()
    plt.show()
