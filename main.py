import logging
import pickle
import warnings

import multiprocessing_logging
from scipy.integrate import IntegrationWarning
from scipy.optimize import OptimizeWarning

from conf.config import Config

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=IntegrationWarning)

logging.basicConfig(
    filename='logs/main.log',
    level=logging.INFO,
    format="%(asctime)s %(name)-20s %(levelname)-8s %(message)s",
)
multiprocessing_logging.install_mp_handler()
log = logging.getLogger(__name__)


def main(cfg=Config()):
    log.info('Starting main')
    # print(lognormal(np.array(cfg.set_data(22, False, 4).df)))


    # results = cfg.run_batch(18).run_parallel(
    #     'lognormal in beta',
    #     'gamma in beta',
    #     'lognormal',
    #     'inv gamma',
    #     'gamma full fit',
    #     'lognormal full fit',
    #     res=15,
    #     # plot=True,
    #     # save=True,
    #     results=True,
    # )
    #
    # store_results(results)

    # plot_combined(open_results(), save=True)

    # results = open_results()


def store_results(results: dict, file: str = 'Results/dict.pickle'):
    with open(file, 'wb') as f:
        pickle.dump(results, f)


def open_results(file: str = 'Results/dict.pickle') -> dict:
    with open(file, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    main()
