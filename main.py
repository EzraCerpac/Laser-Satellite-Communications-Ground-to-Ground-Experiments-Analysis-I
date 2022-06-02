import logging
import pickle
import sys
import time
import warnings

import multiprocessing_logging
from scipy.integrate import IntegrationWarning
from scipy.optimize import OptimizeWarning

from conf.config import Config
from plotting.fitment_comparison import to_table

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
    # np.random.seed(2)

    # fourier_comparison(np.array(cfg.set_data(18, False, 4).df))
    # fourier_comparison(np.array(cfg.set_data(18, True, 16).df)[:-1])

    """Fitting to generated data"""
    # cfg.set_data()
    # cfg.data.df = data[1]
    # results = cfg.run_batch().run_single(cfg.data,
    #                                      # 'lognormal in beta',
    #                                      # 'gamma in beta',
    #                                      # 'beta',
    #                                      # 'lognormal',
    #                                      # 'inv gamma',
    #                                      # 'gamma full fit',
    #                                      # 'lognormal full fit',
    #                                      'lognormal paper',
    #                                      'lognormal paper true',
    #                                      res=100,
    #                                      plot=True,
    #                                      # save=True,
    #                                      # results=True,
    #                                      )
    # cfg.set_data()
    # cfg.data.df = data[2]
    # results = cfg.run_batch().run_single(cfg.data,
    #                                      # 'lognormal in beta',
    #                                      # 'gamma in beta',
    #                                      'beta',
    #                                      # 'lognormal',
    #                                      # 'inv gamma',
    #                                      # 'gamma full fit',
    #                                      # 'lognormal full fit',
    #                                      res=100,
    #                                      plot=True,
    #                                      # save=True,
    #                                      # results=True,
    #                                      )
    # generated_data_analysis(cfg, 10)

    """Fitting to given data"""
    # results = cfg.run_batch(18, 22).run_parallel(
    #     'lognormal in beta',
    #     # 'gamma in beta',
    #     # 'lognormal',
    #     # 'inv gamma',
    #     # 'gamma full fit',
    #     # 'lognormal full fit',
    #     # 'combined paper',
    #     'combined',
    #     res=100,
    #     plot=True,
    #     save=True,
    #     results=True,
    # )
    # # results = cfg.run_batch().run_single(
    # #     cfg.set_data(18, True, 16),
    # #     # 'lognormal in beta',
    # #     # 'gamma in beta',
    # #     # 'lognormal',
    # #     # 'inv gamma',
    # #     # 'gamma full fit',
    # #     # 'lognormal full fit',
    # #     'combined paper',
    # #     'combined',
    # #     res=30,
    # #     plot=True,
    # #     # save=True,
    # #     # results=True,
    # # )
    # pprint(results)
    # store_results(results)
    # pprint(open_results())

    # plot_combined(open_results(), save=False)
    print(to_table('Results/last.pickle'))

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
