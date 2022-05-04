import pickle
import warnings

from scipy.integrate import IntegrationWarning

from conf.config import Config
from conf.plotting import plot_combined

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=IntegrationWarning)


def main(cfg=Config()):
    # print(lognormal(np.array(cfg.set_data(22, False, 4).df)))

    results = cfg.run_batch(18).run_parallel(
        # 'lognormal in beta',
        # 'gamma in beta',
        # 'lognormal',
        # 'inv gamma',
        'gamma full fit',
        res=2,
        plot=True,
        errors=False,
        save=False,
        results=True)

    print(results)
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
