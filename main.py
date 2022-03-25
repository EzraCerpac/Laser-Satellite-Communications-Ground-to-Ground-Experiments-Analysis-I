import warnings

from conf.config import Config

warnings.filterwarnings("ignore", category=RuntimeWarning)


def main(cfg=Config()):
    # cfg.set_data(18, True, 8)
    # cfg.run().calc_sigma(plot=True)
    print(cfg.run_batch([18]).run('sigma', 'sigma better', plot=False))
    # estimate_sigma_better(np.array(cfg.set_data(18, False, 3).df), 18, plot=True)
    # plt.show()


if __name__ == "__main__":
    main()
