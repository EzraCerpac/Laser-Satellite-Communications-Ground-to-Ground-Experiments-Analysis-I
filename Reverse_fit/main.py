from scipy.optimize import curve_fit
import numpy as np
from Model.with_beta import combined_dist
from matplotlib import pyplot as plt
from plotting.norm_I_hist import norm_I_hist
from Model.with_beta import combined_dist
import pandas as pd


def full_fit_lognorm(I: np.ndarray, res: float, plot: bool):
    yy = norm_I_hist(I, bins=res, plot=plot)
    xx = np.linspace(1e-10, 1, len(yy))
    (alpha, beta, I_0), p_cov = curve_fit(combined_dist, xx, yy, scale=1)
    if plot:
        xx = np.linspace(1e-15, 1, 1001)
        plt.plot(xx, (xx, alpha, beta, I_0))

    return (alpha, beta, I_0), p_cov



def Jorensfit(I):
    results = curve_fit(combined_dist, I, np.histogram(I))

    return results

