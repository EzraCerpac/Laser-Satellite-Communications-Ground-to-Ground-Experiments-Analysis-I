import pickle
import warnings

from conf.config import Config

warnings.filterwarnings("ignore", category=RuntimeWarning)


def main(cfg=Config()):
    # print(lognormal(np.array(cfg.set_data(22, False, 4).df)))
    #
    results = cfg.run_batch(18, 22).run_parallel(
        'sigma_with_alpha',
        'sigma_gamma_with_alpha',
        'lognormal',
        'inv gamma',
        plot=True, save=True
    )
    print(results)
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
