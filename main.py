import pickle
import warnings

from conf.config import Config

warnings.filterwarnings("ignore", category=RuntimeWarning)


def main(cfg=Config()):
    # estimate_sigma(np.array(cfg.set_data(18, True, 4).df), 18, False, 10, plot=True)

    results = cfg.run_batch(18).run('sigma', 'sigma gamma', plot=True, save=False)
    # store_results(results)

    # results = open_results()


def store_results(results: dict, file: str = 'Results/sigmas.pickle'):
    with open(file, 'wb') as f:
        pickle.dump(results, f)


def open_results(file: str = 'Results/sigmas.pickle') -> dict:
    with open(file, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    main()
