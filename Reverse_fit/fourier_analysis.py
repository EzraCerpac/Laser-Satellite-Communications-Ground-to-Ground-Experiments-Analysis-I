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
    # pcomb = norm_I(Pcomb(  # 18 off 4
    #     scint_psi=1.8,
    #     mean_received_power=.749,
    #     beam_divergence=10 ** -(4.7),
    #     pointing_jitter=10 ** (-9),
    #     scint_bandwith=10,
    #     jit_bandwith=10,
    #     scint_slope=20,
    #     jit_slope=20,
    #     sampling_freq=2478.9,
    #     vector_length=30
    # ))
    pcomb = norm_I(Pcomb(  # 18 on 16
        scint_psi=1.8 * 1.38,
        mean_received_power=.749,  # np.mean(data),
        beam_divergence=10 ** -(4.7),
        pointing_jitter=10 ** (-8.5),
        scint_bandwith=10,
        jit_bandwith=10,
        scint_slope=20,
        jit_slope=20,
        sampling_freq=2478.9,
        vector_length=30
    ))

    # t_comp(data, pcomb)
    fft_comp(data, pcomb)
    # hist_comp(data, pcomb)
    # memory_check(data, pcomb)


def memory_check(data, pcomb):
    t = np.arange(0, 30, 1 / 2478.9)
    plt.plot(t, pcomb, label='data')
    plt.plot(t, spline_regression(t, pcomb), color='red', label='spline')
    plt.xlabel(r'$t$ [s]')
    plt.ylabel(r'$I_n$ [-]')
    plt.legend()
    plt.show()
    plt.plot(t, data, label='data')
    plt.plot(t, spline_regression(t, data), color='red', label='spline')
    plt.xlabel(r'$t$ [s]')
    plt.ylabel(r'$I_n$ [-]')
    plt.legend()
    plt.show()


def spline_regression(t, y):
    from scipy.interpolate import UnivariateSpline
    spl = UnivariateSpline(t, y, s=len(t) // 60)
    return spl(t)


def hist_comp(data, pcomb):
    plt.hist(data, bins=100, density=True, color='blue', histtype='stepfilled', alpha=0.5, label='real')
    plt.hist(pcomb, bins=100, density=True, color='red', histtype='stepfilled', alpha=0.5, label='generated')
    plt.legend(loc='upper right')
    plt.xlabel(r'$I_n$ [-]')
    plt.ylabel('PDF')
    plt.show()


def t_comp(data, pcomb):
    t = np.arange(0, 30, 1 / 2478.9)
    plt.plot(t, pcomb, color='red', label='generated', alpha=0.5)
    plt.plot(t, data, color='blue', label='real', alpha=0.5)
    plt.xlabel(r'$t$ [s]')
    plt.ylabel(r'$I_n$ [-]')
    plt.legend(loc='upper right')
    plt.show()


def fft_comp(data, pcomb):
    fft1 = fft(pcomb)
    fft2 = fft(data)
    plt.loglog(fftfreq(fft1.size, d=1 / 2478.9), np.abs(fft1), color='red', label='PVGeT generated', alpha=0.5)
    plt.loglog(fftfreq(fft2.size, d=1 / 2478.9), np.abs(fft2), color='blue', label='low turbulance, modes off',
               alpha=0.5)
    # plt.ylim(0, 50)
    # plt.xlim(0, 1000)
    plt.legend(loc='upper right')
    plt.xlabel(r'$f$ [Hz]')
    plt.ylabel(r'$I_n$ [W/m$^2$]')
    plt.show()
