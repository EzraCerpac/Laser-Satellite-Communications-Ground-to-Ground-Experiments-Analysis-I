import warnings

from conf.config import FileConfig

warnings.filterwarnings("ignore", category=RuntimeWarning)


def main(cfg=FileConfig()):
    # cfg.set_data(18, True, 8)
    # cfg.run().calc_sigma(plot=True)
    print(cfg.run_batch([18]).run('sigma'))


if __name__ == "__main__":
    main()
