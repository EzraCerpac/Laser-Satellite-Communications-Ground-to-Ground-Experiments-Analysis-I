from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from PVGeT.jitter_gen import Pjit
from PVGeT.scint_gen import Psci


def Pcomb(*, scint_psi, mean_received_power, beam_divergence, pointing_jitter, scint_bandwith, jit_bandwith,
          scint_slope, jit_slope, sampling_freq, vector_length, return_scint_sub=False) -> np.ndarray | tuple[
    np.ndarray, np.ndarray, np.ndarray]:
    """
    Generates the combined power spectrum of the scintillator and jitter.

    """
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
    return (P_comb, P_sci, P_jit) if return_scint_sub else P_comb


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
    Pcomb(
        scint_psi=0.18,
        mean_received_power=.749,
        beam_divergence=18e-6,
        pointing_jitter=1e-9,  # sigma_jit,
        scint_bandwith=900,
        jit_bandwith=900,
        scint_slope=90,
        jit_slope=80,
        sampling_freq=8e3,
        vector_length=100
    )
    # plt.hist(P_sci, bins=100, histtype='step', label='P_sci')
    # plt.hist(P_jit, bins=100, histtype='step', label='P_jit')
    # plt.hist(P_comb, bins=100, histtype='step', label='P_comb')
    # plt.plot(P_sci, label='P_sci')
    # plt.plot(P_jit, label='P_jit')
    # plt.plot(P_comb, label='P_comb')
    plt.legend()
    # plt.ylim(2.1, 2.125)
    plt.show()
