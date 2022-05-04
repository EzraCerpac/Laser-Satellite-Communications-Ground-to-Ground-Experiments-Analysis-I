import pickle
import warnings

from conf.config import Config
from plotting.fitment_comparison import comparison_plot
from Fade.fade_loss import fade_loss_plots
from combined_fit.angular_jitter_fit_gamma import gamma_gamma
from Fade.fade_loss_theoretical import PDF_gamma_test

warnings.filterwarnings("ignore", category=RuntimeWarning)


def main(cfg=Config()):
    # print(lognormal(np.array(cfg.set_data(22, False, 4).df)))

    #
    # results = cfg.run_batch(18, 22).run_parallel(
    #     # 'lognormal in beta',
    #     # 'gamma in beta',
    #     'lognormal',
    #     'inv gamma',
    #     plot=False, save=False, results=True
    # )

    # print(results)
    # store_results(results)
    #
    # comparison_plot()
    # fade_loss_plots()
    # print(PDF_gamma())
    PDF_gamma_test()

    #print(gamma_gamma(1, 1))

    # results = open_results()


def store_results(results: dict, file: str = 'Results/dict.pickle'):
    with open(file, 'wb') as f:
        pickle.dump(results, f)


def open_results(file: str = 'Results/dict.pickle') -> dict:
    with open(file, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    main()
