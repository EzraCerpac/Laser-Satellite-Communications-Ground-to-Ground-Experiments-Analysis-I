import pandas as pd
from matplotlib import pyplot as plt

from conf.config import FileConfig


def main(cfg=FileConfig()):
    # df = pd.read_pickle(cfg.df.dir + cfg.df.data11.dir + str(cfg.df.data11.mode.number[0]) + cfg.df.data11.extension)
    df = pd.read_pickle(cfg.default.file)
    df.plot()
    plt.show()


if __name__ == "__main__":
    main()
