import warnings

import numpy as np

from Model.main import main2
from conf.config import Config

warnings.filterwarnings("ignore", category=RuntimeWarning)


def main(cfg=Config()):
    # cfg.set_data(18, True, 8)
    # cfg.run().calc_sigma(plot=True)
    # print(cfg.run_batch([18]).run('sigma', plot=True))
    main2(np.array(cfg.set_data(18, True, 16).df))

if __name__ == "__main__":
    main()
