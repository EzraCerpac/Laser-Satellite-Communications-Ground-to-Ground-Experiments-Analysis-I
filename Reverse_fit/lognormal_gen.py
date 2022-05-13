import numpy as np
from scipy.signal import butter, lfilter,


def Psci(psi, cut_off_freq, lpf_slope, sampling_freq, vector_length, mean_received_power):
    X1 = random_variable_generation(vector_length // sampling_freq)
    X1_f = LPF(X1, cut_off_freq, lpf_slope)


def random_variable_generation(size: int) -> np.ndarray:
    return np.random.normal(0, 1, size)


def LPF(X1, cut_off_freq, lpf_slope):
    """Butterworth low pass filter"""
    b, a = butter(1, cut_off_freq / (0.5 * len(X1)), btype='low', analog=False, output='ba')
    X1_f = lfilter(b, a, X1)
    return X1_f
