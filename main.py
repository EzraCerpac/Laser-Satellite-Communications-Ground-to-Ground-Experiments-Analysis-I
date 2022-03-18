from conf.config import FileConfig


def main(cfg=FileConfig()):
    cfg.data_set(18, False, 1)
    cfg.run().calc_sigma(plot=True)
    cfg.data_set(18, False, 2)
    cfg.run().calc_sigma(plot=True)
    cfg.data_set(18, False, 3)
    cfg.run().calc_sigma(plot=True)
    cfg.data_set(18, False, 4)
    cfg.run().calc_sigma(plot=True)
    cfg.data_set(18, False, 5)
    cfg.run().calc_sigma(plot=True)
    cfg.data_set(18, True, 2)
    cfg.run().calc_sigma(plot=True)
    cfg.data_set(18, True, 4)
    cfg.run().calc_sigma(plot=True)
    cfg.data_set(18, True, 8)
    cfg.run().calc_sigma(plot=True)
    cfg.data_set(18, True, 16)
    cfg.run().calc_sigma(plot=True)
    cfg.data_set(18, True, 28)
    cfg.run().calc_sigma(plot=True)


if __name__ == "__main__":
    main()
