import logging
import pickle
import sys
import time
import warnings

import multiprocessing_logging
from scipy.integrate import IntegrationWarning

from conf.config import Config

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=IntegrationWarning)

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
    # print(lognormal(np.array(cfg.set_data(22, False, 4).df)))

    results = cfg.run_batch(18).run_parallel(
        'lognormal in beta',
        'gamma in beta',
        'lognormal',
        'inv gamma',
        'gamma full fit',
        'lognormal full fit',
        res=5,
        plot=True,
        errors=False,
        save=True,
        results=True
    )

    print(results)
    store_results(results)

    # plot_combined(open_results(), save=False)
    # comparison_plot()
    # results = open_results()


def store_results(results: dict, file: str = 'Results/dict.pickle'):
    with open(file, 'wb') as f:
        pickle.dump(results, f)


def open_results(file: str = 'Results/dict.pickle') -> dict:
    with open(file, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    main()
