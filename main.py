from conf.config import FileConfig


def main(cfg=FileConfig()):
    cfg.data_set(18, True, 4)
    cfg.run().calc_sigma(plot=True)


if __name__ == "__main__":
    main()
