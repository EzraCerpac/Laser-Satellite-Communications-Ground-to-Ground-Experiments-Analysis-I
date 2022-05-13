import logging
from typing import Dict

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import invgamma, lognorm

from Model.inv_gamma import inv_gamma, inv_gamma_curve_fit
from Model.pure_lognormal import lognormal, lognormal_curve_fit
from Model.with_beta import estimate_sigma as estimate_sigma_with_alpha
from conf.data import Data

log = logging.getLogger(__name__)

Result = Dict[int, Dict[bool, Dict[int, Dict[str, float]]]]


class Run:
    def __init__(self, data: Data):
        self.data = data
        self.results = {}

    def fit_lognormal_in_beta(self, res: int = 101, plot: bool = False, **unused):
        self.results['lognormal in beta'] = {}
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, False, res, plot)
        self.results['lognormal in beta']['sigma'] = result[0]
        self.results['lognormal in beta']['alpha'] = result[1]
        self.results['lognormal in beta']['beta'] = result[2]
        self.results['lognormal in beta']['standard div'] = result[-1]
        return self.results

    def fit_gamma_in_beta(self, res: int = 101, plot: bool = False, **unused):
        self.results['gamma in beta'] = {}
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, True, res, plot)
        self.results['gamma in beta']['sigma'] = result[0]
        self.results['gamma in beta']['alpha'] = result[1]
        self.results['gamma in beta']['beta'] = result[2]
        self.results['gamma in beta']['standard div'] = result[-1]
        return self.results

    def fit_lognormal(self, plot: bool = False, **unused):
        self.results['lognormal'] = {}
        result1 = lognormal(np.array(self.data.df), plot=False)
        result2 = lognormal_curve_fit(np.array(self.data.df), plot=False)
        result = result1 if result1[-1] < result2[-1] else result2
        self.results['lognormal']['skew'] = result[0]
        self.results['lognormal']['pos'] = result[1]
        self.results['lognormal']['standard div'] = result[-1]
        if plot:
            plt.plot(xx := np.linspace(1e-5, 1, 1001), lognorm.pdf(xx, result[0], result[1]), label='lognormal fitment')
        return self.results

    def fit_inv_gamma(self, plot: bool = False, **unused):
        self.results['inv gamma'] = {}
        result1 = inv_gamma(np.array(self.data.df), plot=False)
        result2 = inv_gamma_curve_fit(np.array(self.data.df), plot=False)
        result = result1 if result1[-1] < result2[-1] else result2
        self.results['inv gamma']['a'] = result[0]
        self.results['inv gamma']['pos'] = result[1]
        self.results['inv gamma']['standard div'] = result[-1]
        if plot:
            plt.plot(xx := np.linspace(1e-5, 1, 1001), invgamma.pdf(xx, result[0], result[1]),
                     label='inverse gamma fitment')
        return self.results

    def calc_full_lognorm(self, res: int = 101, plot: bool = False, **unused):
        self.results['lognormal full fit'] = {}
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, False, res, plot, full_fit=True)
        self.results['lognormal full fit']['sigma'] = result[0]
        self.results['lognormal full fit']['alpha'] = result[1]
        self.results['lognormal full fit']['beta'] = result[2]
        self.results['lognormal full fit']['sigma_i'] = result[3]
        self.results['lognormal full fit']['standard div'] = result[-1]
        return self.results

    def calc_full_gamma_in_beta(self, res: int = 101, plot: bool = False, **unused):
        self.results['gamma full fit'] = {}
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, True, res, plot, full_fit=True)
        self.results['gamma full fit']['sigma'] = result[0]
        self.results['gamma full fit']['alpha'] = result[1]
        self.results['gamma full fit']['beta'] = result[2]
        self.results['gamma full fit']['a'] = result[3]
        self.results['gamma full fit']['b'] = result[4]
        self.results['gamma full fit']['standard div'] = result[-1]
        return self.results


