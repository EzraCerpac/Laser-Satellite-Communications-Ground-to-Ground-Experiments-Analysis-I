import logging
import pickle
import sys
import time
import warnings

import multiprocessing_logging
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import IntegrationWarning
from scipy.optimize import OptimizeWarning

from Reverse_fit.comb_gen import Pcomb
from Reverse_fit.fourier_analysis import fourier_comparison
from conf.config import Config
from formula.normalize import norm_I

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=IntegrationWarning)
warnings.filterwarnings("ignore", category=OptimizeWarning)

file_handler = logging.FileHandler(filename=f'logs/{time.strftime("%d-%m-%Y")}.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-20s %(levelname)-8s %(message)s",
    handlers=handlers,
)
multiprocessing_logging.install_mp_handler()
log = logging.getLogger(__name__)


def main(cfg=Config()):
    log.info('Starting main')
    np.random.seed(2)

    # fourier_comparison(np.array(cfg.set_data(18, False, 4).df))

    """Fitting to generated data"""
    # data = norm_I(Pcomb(
    #         scint_psi=1.8,
    #         mean_received_power=.749,
    #         beam_divergence=10 ** -4.7,
    #         pointing_jitter=10**(-9),
    #         scint_bandwith=10,
    #         jit_bandwith=10,
    #         scint_slope=20,
    #         jit_slope=20,
    #         sampling_freq=2478.9,
    #         vector_length=30
    #     ))
    # cfg.set_data()
    # cfg.data.df = data
    # plt.hist(data, bins=100, label='P_sci')
    # plt.show()
    # results = cfg.run_batch().run_single(cfg.data,
    #     'lognormal in beta',
    #     'gamma in beta',
    #     #'lognormal',
    #     #'inv gamma',
    #     #'gamma full fit',
    #     #'lognormal full fit',
    #     res=12,
    #     plot=True,
    #     # save=True,
    #     # results=True,
    # )
    # print(results)
    #
    # plt.legend()
    # plt.show()

    """Fitting to given data"""
    results = cfg.run_batch(18).run_parallel(
        # 'lognormal in beta',
        # 'gamma in beta',
        'lognormal',
        'inv gamma',
        # 'gamma full fit',
        # 'lognormal full fit',
        res=2,
        plot=True,
        # save=True,
        # results=True,
    )

    # store_results(results)

    # plot_combined(open_results(), save=False)
    # comparison_plot('Results/11-05-2022_to_use_full_fit.pickle', save=True)
    #
    # irradiance_plot(pd.read_csv('Data/CSV/data18urad.csv'), save=True)
    # build_up_plots(open_results('Results/13-05-2022.pickle'), 'lognormal in beta', save=False)


def store_results(results: dict, file: str = 'Results/dict.pickle'):
    with open(file, 'wb') as f:
        pickle.dump(results, f)


def open_results(file: str = 'Results/dict.pickle') -> dict:
    with open(file, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Log exception with traceback
        log.critical(e, exc_info=True)
