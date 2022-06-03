import logging
from typing import Dict

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import invgamma, lognorm, beta

from Fade.data_fade import plot_fade_prob, plot_fade_count, plot_mean_time
from Model.inv_gamma import inv_gamma, inv_gamma_curve_fit
from Model.lognormal_paper_based import lognormal_paper_curve_fit, lognormal_paper, lognormal_paper_true_curve_fit, \
    lognormal_paper_true
from Model.pure_beta import beta_curve_fit
from Model.pure_combined import combined_curve_fit, combined_paper_curve_fit, func_paper
from Model.pure_lognormal import lognormal, lognormal_curve_fit
from Model.with_beta import estimate_sigma as estimate_sigma_with_alpha
from conf.data import Data

log = logging.getLogger(__name__)

Result = Dict[int, Dict[bool, Dict[int, Dict[str, float]]]]


class Run:
    def __init__(self, data: Data):
        self.data = data
        self.results = {}

    def fit_lognormal_in_beta(self, res: int = 10, plot: bool = False, **unused):
        self.results['lognormal in beta'] = {}
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, False, res, plot)
        self.results['lognormal in beta']['sigma'] = result[0]
        self.results['lognormal in beta']['alpha'] = result[1]
        self.results['lognormal in beta']['beta'] = result[2]
        self.results['lognormal in beta']['standard div'] = result[-1]
        return self.results

    def fit_gamma_in_beta(self, res: int = 10, plot: bool = False, **unused):
        self.results['gamma in beta'] = {}
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, True, res, plot)
        self.results['gamma in beta']['sigma'] = result[0]
        self.results['gamma in beta']['alpha'] = result[1]
        self.results['gamma in beta']['beta'] = result[2]
        self.results['gamma in beta']['standard div'] = result[-1]
        return self.results

    def fit_beta(self, plot: bool = False, **unused):
        self.results['beta'] = {}
        # result1 = beta_fit(np.array(self.data.df), plot=False)
        result = beta_curve_fit(np.array(self.data.df), plot=False)
        # result = result1 if result1[-1] < result2[-1] else result2
        self.results['beta']['a'] = result[0]
        self.results['beta']['b'] = result[1]
        self.results['beta']['standard div'] = result[-1]
        if plot:
            plt.plot(xx := np.linspace(1e-5, 1, 1001), beta.pdf(xx, result[0], result[1]), label='beta fitment')
        return self.results

    def fit_combined(self, plot: bool = False, **unused):
        self.results['combined'] = {}
        # result1 = beta_fit(np.array(self.data.df), plot=False)
        result = combined_curve_fit(np.array(self.data.df), plot=False)
        # result = result1 if result1[-1] < result2[-1] else result2
        self.results['combined']['a'] = result[0]
        self.results['combined']['b'] = result[1]
        self.results['combined']['c'] = result[2]
        self.results['combined']['standard div'] = result[-1]
        if plot:
            plt.plot(xx := np.linspace(1e-5, 1, 1001), beta.pdf(xx, result[0], result[1]), label='beta fitment')
        return self.results

    def fit_combined_paper(self, plot: bool = False, **unused):
        self.results['combined paper'] = {}
        # result1 = beta_fit(np.array(self.data.df), plot=False)
        result = combined_paper_curve_fit(np.array(self.data.df), plot=False)
        # result = result1 if result1[-1] < result2[-1] else result2
        self.results['combined paper']['sigma_i2'] = result[0]
        self.results['combined paper']['I_0'] = result[2]
        self.results['combined paper']['beta_b'] = result[1]
        self.results['combined paper']['standard div'] = result[-1]
        if plot:
            plt.plot(xx := np.linspace(1e-5, 1, 1001), func_paper(xx, result[0], result[1], result[2]),
                     label='combined paper fitment')
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

    def fit_lognormal_paper(self, plot: bool = False, **unused):
        self.results['lognormal paper'] = {}
        result = lognormal_paper_curve_fit(np.array(self.data.df), plot=False)
        self.results['lognormal paper']['sigma_i'] = result[0]
        self.results['lognormal paper']['mu'] = result[1]
        self.results['lognormal paper']['I_0'] = result[2]
        self.results['lognormal paper']['standard div'] = result[-1]
        if plot:
            plt.plot(xx := np.linspace(1e-5, 1, 1001), lognormal_paper(xx, result[0], result[1]), label='lognormal paper fitment')
        return self.results


    def fit_lognormal_paper_true(self, plot: bool = False, **unused):
        self.results['lognormal paper true'] = {}
        result = lognormal_paper_true_curve_fit(np.array(self.data.df), plot=False)
        self.results['lognormal paper true']['sigma_i'] = result[0]
        self.results['lognormal paper true']['I_0'] = result[1]
        #self.results['lognormal paper true']['x scale'] = result[1]
        self.results['lognormal paper true']['standard div'] = result[-1]
        if plot:
            plt.plot(xx := np.linspace(1e-5, 1, 1001), lognormal_paper_true(xx, result[0], result[1]), label='lognormal paper true fitment')
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

    def calc_full_lognorm(self, res: int = 10, plot: bool = False, **unused):
        self.results['lognormal full fit'] = {}
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, False, res, plot, full_fit=True)
        self.results['lognormal full fit']['sigma'] = result[0]
        self.results['lognormal full fit']['alpha'] = result[1]
        self.results['lognormal full fit']['beta'] = result[2]
        self.results['lognormal full fit']['sigma_i'] = result[3]
        self.results['lognormal full fit']['standard div'] = result[-1]
        return self.results

    def calc_full_gamma_in_beta(self, res: int = 10, plot: bool = False, **unused):
        self.results['gamma full fit'] = {}
        result = estimate_sigma_with_alpha(np.array(self.data.df), self.data.w_0, True, res, plot, full_fit=True)
        self.results['gamma full fit']['sigma'] = result[0]
        self.results['gamma full fit']['alpha'] = result[1]
        self.results['gamma full fit']['beta'] = result[2]
        self.results['gamma full fit']['a'] = result[3]
        self.results['gamma full fit']['b'] = result[4]
        self.results['gamma full fit']['standard div'] = result[-1]
        return self.results

    def fade_prob_data(self, res: int = 10, plot: bool = False, **unused):
        self.results['fade probability data'] = {}
        result = plot_fade_prob(np.array(self.data.df), res, plot)
        self.results['fade probability data']['F_t'] = result[0]
        self.results['fade probability data']['Prob'] = result[1]
        self.results['fade probability data']['Min'] = result[2]
        self.results['fade probability data']['Max'] = result[3]
        return self.results

    def fade_count_data(self, res: int = 10, plot: bool = False, **unused):
        self.results['fade count data'] = {}
        result = plot_fade_count(np.array(self.data.df), res, plot)
        self.results['fade count data']['F_t'] = result[0]
        self.results['fade count data']['Time'] = result[1]
        self.results['fade count data']['Min'] = result[2]
        self.results['fade count data']['Max'] = result[3]
        return self.results

    def fade_mean_data(self, res: int = 10, plot: bool = False, **unused):
        self.results['fade mean time data'] = {}
        result = plot_mean_time(np.array(self.data.df), res, plot)
        self.results['fade mean time data']['F_t'] = result[0]
        self.results['fade mean time data']['Time'] = result[1]
        self.results['fade mean time data']['Min'] = result[2]
        self.results['fade mean time data']['Max'] = result[3]
        return self.results
