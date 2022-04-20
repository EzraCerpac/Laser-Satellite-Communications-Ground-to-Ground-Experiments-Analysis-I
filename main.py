import pickle
import warnings

from conf.config import Config

warnings.filterwarnings("ignore", category=RuntimeWarning)


def main(cfg=Config()):
    # plt.plot(np.array(cfg.set_data(18, True, 4).df))
    # plt.show()
    # cfg.run().calc_sigma_gamma(plot=True)

    print(cfg.run_batch([18]).run('sigma', 'sigma gamma', plot=True, save=True))

    # test()
    # results = open_results()
    # sigmaplot(results)


def store_results(cfg=Config()):
    with open('Results/sigmas.pickle', 'wb') as f:
        pickle.dump(cfg.run_batch([18]).run('sigma'), f)


def open_results(file: str = 'Results/sigmas.pickle') -> dict:
    with open(file, 'rb') as f:
        return pickle.load(f)
    # print(cfg.run_batch([18]).run('sigma', plot=True))


if __name__ == "__main__":
    main()
