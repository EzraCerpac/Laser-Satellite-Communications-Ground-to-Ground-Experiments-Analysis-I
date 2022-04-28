import numpy as np
from scipy.fft import fft, fftfreq


def fourier_test(data: np.ndarray):
    N = len(data)
    yf = fft(data)
    xf = fftfreq(N, 1 / N)[:N // 2]
    import matplotlib.pyplot as plt
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
    plt.show()
