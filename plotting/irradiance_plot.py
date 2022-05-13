import matplotlib.pyplot as plt
import pandas as pd

# starting_values_18 = {
#     'off1': 38.,
#     '2 modes': 100.0,
#     'off2': 154.,
#     '28 modes': 270.,
#     'off3': 341.,
#     '4 modes': 416.,
#     'off4': 487.,
#     '8 modes': 564.,
#     'off5': 636.,
#     '16 modes': 668.
# }

starting_values_18 = {
    'off': 46.3,
    '2\nmodes': 100.0,
    'off ': 172.3,
    '28\nmodes': 240.3,
    'off  ': 318.1,
    # '4\nmodes': 382.0,
    # 'off   ': 472.9,
    # '8\nmodes': 527.6,
    # 'off    ': 603.3,
    # '16\nmodes': 675.2
}


def irradiance_plot(irradiance: pd.DataFrame, save=False, path='Plots/irradiance_plot.pdf'):
    """
    Plot irradiance data.
    """
    # plt.figure(figsize=(8, 5))
    irradiance.plot(kind='line', x='time', y='irradiance', legend=False)
    plt.xlabel('$t$ [s]')
    plt.ylabel('$I$ [W/m$^2$]')
    plt.xlim(0, 400)
    plt.ylim(0, irradiance['irradiance'].max())
    for mode, start in starting_values_18.items():
        plt.axvline(start, color='k', linestyle='--')
        plt.text(start + 15, irradiance['irradiance'].max() * 1.01, mode, va='bottom', ha='center', rotation=0)
        plt.axvline(start + 30, color='r', linestyle='--')
    plt.legend(['irradiance', 'interval start', 'interval stop'])
    if save:
        plt.savefig(path)
    plt.show()
