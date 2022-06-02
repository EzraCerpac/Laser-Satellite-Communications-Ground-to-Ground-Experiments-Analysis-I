import numpy as np
from scipy.signal import butter, filtfilt


def random_variable_generation(m, s, size: int) -> np.ndarray:
    return np.random.normal(m, s, size)


def LPF(X, cut_off_freq, lpf_slope, sampling_freq):
    """Butterworth low pass filter"""
    nyquist_freq = 0.5 * sampling_freq
    N = lpf_slope // 20
    b, a = butter(N, cut_off_freq / nyquist_freq)
    X_f = filtfilt(b, a, X)
    return X_f
