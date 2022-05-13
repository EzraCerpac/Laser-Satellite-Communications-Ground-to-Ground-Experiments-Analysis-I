import matplotlib.pyplot as plt
import numpy as np

from Reverse_fit.jitter_gen import Pjit
from Reverse_fit.scint_gen import Psci


def Pcomb(*, scint_psi, mean_received_power, beam_divergence, pointing_jitter, scint_bandwith, jit_bandwith,
          scint_slope, jit_slope, sampling_freq, vector_length):
    P_sci = Psci(
        psi=scint_psi,
        cut_off_freq=scint_bandwith,
        lpf_slope=scint_slope,
        sampling_freq=sampling_freq,
        vector_length=vector_length,
        mean_received_power=mean_received_power,
    )
    P_jit = Pjit(
        beam_divergence=beam_divergence,
        pointing_jitter=pointing_jitter,
        cut_off_freq=jit_bandwith,
        lpf_slope=jit_slope,
        sampling_freq=sampling_freq,
        vector_length=vector_length,
    )
    P_comb = P_sci * P_jit

    plt.hist(P_sci, bins=100, histtype='step', label='P_sci')
    plt.hist(P_jit, bins=100, histtype='step', label='P_jit')
    plt.hist(P_comb, bins=100, histtype='step', label='P_comb')
    plt.legend()
    plt.show()
    return P_comb


if __name__ == '__main__':
    np.random.seed(0)
    omega_0 = 18e-9
    beta_jit = 2.16
    sigma_jit = np.sqrt(omega_0 ** 2 / (4 * beta_jit))
    # Pcomb(
    #     psi=0.34,
    #     mean_received_power=.749,
    #     beam_divergence=4.6,
    #     pointing_jitter=sigma_jit,
    #     cut_off_freq=30,
    #     lpf_slope=41,
    #     sampling_freq=8e3,
    #     vector_length=100,
    # )
    Pcomb(scint_psi=0.18, mean_received_power=.749, beam_divergence=4.6, pointing_jitter=sigma_jit, scint_bandwith=15,
          jit_bandwith=26, scint_slope=20, jit_slope=16, sampling_freq=8e3, vector_length=100)
