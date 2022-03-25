import pickle
import warnings

from combined_fit.Plotting.plots import sigmaplot
import numpy as np

from conf.config import Config

warnings.filterwarnings("ignore", category=RuntimeWarning)


def main(cfg=Config()):
    # cfg.set_data(18, True, 8)
    # cfg.run().calc_sigma(plot=True)
    # cfg.run_batch([18]).run('sigma')

    results = open_results()
    sigmaplot(results)

def store_results(cfg=Config()):
    with open('Results/sigmas.pickle', 'wb') as f:
        pickle.dump(cfg.run_batch([18]).run('sigma'), f)

def open_results(file: str = 'Results/sigmas.pickle') -> dict:
    with open(file, 'rb') as f:
        return pickle.load(f)
    # print(cfg.run_batch([18]).run('sigma', plot=True))

if __name__ == "__main__":
    main()
