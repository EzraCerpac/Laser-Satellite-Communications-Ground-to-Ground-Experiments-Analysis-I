import numpy as np
from matplotlib import pyplot as plt
from numpy.fft import fftfreq
from scipy.fft import fft

from Reverse_fit.comb_gen import Pcomb
from formula.normalize import norm_I

# set matplotlib color to set1
plt.style.use('seaborn-colorblind')


def fourier_comparison(data):
    data = norm_I(data)
    pcomb = norm_I(Pcomb(
        scint_psi=1.8,
        mean_received_power=.749,
        beam_divergence=10 ** -(4.7),
        pointing_jitter=10 ** (-9),
        scint_bandwith=10,
        jit_bandwith=10,
        scint_slope=20,
        jit_slope=20,
        sampling_freq=2478.9,
        vector_length=30
    ))

    fft1 = fft(pcomb)

    # [plt.hist(var[1], bins=100, density=True, histtype='step', label=var[0]) for var in bds]
    plt.plot(fftfreq(fft1.size, d=1 / 2478.9), np.abs(fft1), color='red', label='PVGeT generated', alpha=0.5)

    fft1 = fft(data)

    # change transparency of plot
    plt.plot(fftfreq(fft1.size, d=1 / 2478.9), np.abs(fft1), color='blue', label='low turbulance, modes off', alpha=0.5)
    plt.ylim(0, 100)
    plt.xlim(0, 1000)
    plt.legend(loc='upper right')
    plt.xlabel(r'$f$ [Hz]')
    plt.ylabel(r'$I_n$ [W/m$^2$]')
    plt.show()
    # t = np.arange(0, 30, 1 / 2478.9)
    #
    # # plt.plot(pcomb, color='red', label='generated', alpha=0.5)
    # # plt.plot(data, color='blue', label='real', alpha=0.5)
    # plt.hist(data, bins=100, density=True, color='blue', histtype='stepfilled', alpha=0.5, label='real')
    # plt.hist(pcomb, bins=100, density=True, color='red', histtype='stepfilled', alpha=0.5, label='generated')
    # plt.legend(loc='upper right')
    # plt.xlabel(r'$I_n$ [-]')
    # plt.ylabel('PDF')
    # plt.show()


if __name__ == '__main__':
    test()
