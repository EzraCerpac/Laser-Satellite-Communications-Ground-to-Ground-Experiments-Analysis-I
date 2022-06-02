from collections import Counter

import pandas as pd

from PVGeT.comb_gen import Pcomb
from formula.normalize import norm_I


def generated_data_analysis(cfg, N=10):
    costs_off = Counter()
    costs_on = Counter()
    for i in range(N):
        data = [norm_I(i) for i in Pcomb(
            scint_psi=1.8,
            mean_received_power=.749,
            beam_divergence=10 ** -(4.7),
            pointing_jitter=10 ** (-9),
            scint_bandwith=10,
            jit_bandwith=10,
            scint_slope=20,
            jit_slope=20,
            sampling_freq=2478.9,
            vector_length=30,
            return_scint_sub=True,
        )]
        cfg.set_data()
        cfg.data.df = data[0]
        results_off = cfg.run_batch().run_single(cfg.data,
                                                 # 'lognormal in beta',
                                                 # 'gamma in beta',
                                                 # 'beta',
                                                 # 'lognormal',
                                                 # 'inv gamma',
                                                 # 'gamma full fit',
                                                 # 'lognormal full fit',
                                                 'combined paper',
                                                 'combined',
                                                 res=10,
                                                 # plot=True,
                                                 # save=True,
                                                 # results=True,
                                                 )
        data = [norm_I(i) for i in Pcomb(
            scint_psi=1.8 * 1.38,
            mean_received_power=.749,  # np.mean(data),
            beam_divergence=10 ** -(4.7),
            pointing_jitter=10 ** (-8.5),
            scint_bandwith=10,
            jit_bandwith=10,
            scint_slope=20,
            jit_slope=20,
            sampling_freq=2478.9,
            vector_length=30,
            return_scint_sub=True,
        )]
        cfg.set_data()
        cfg.data.df = data[0]
        results_on = cfg.run_batch().run_single(cfg.data,
                                                # 'lognormal in beta',
                                                # 'gamma in beta',
                                                # 'beta',
                                                # 'lognormal',
                                                # 'inv gamma',
                                                # 'gamma full fit',
                                                # 'lognormal full fit',
                                                'combined paper',
                                                'combined',
                                                res=10,
                                                # plot=True,
                                                # save=True,
                                                # results=True,
                                                )
        costs_off['Andrews'] += results_off['combined paper']['standard div']
        costs_off['ours'] += results_off['combined']['standard div']
        costs_on['Andrews'] += results_on['combined paper']['standard div']
        costs_on['ours'] += results_on['combined']['standard div']
    df = pd.DataFrame()
    for key, value in costs_off.items():
        df.loc[key, 'modes off'] = value / N
    for key, value in costs_on.items():
        df.loc[key, 'modes on'] = value / N
    print(df.to_latex(
        index=True,
        float_format='%.2e',
        label='tab:TBD',
        caption='Average cost comparison between the different fitments for the PVGeT generation model.',
    ))
