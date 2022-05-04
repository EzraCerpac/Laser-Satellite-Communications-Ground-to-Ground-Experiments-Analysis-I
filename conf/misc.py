# def _label(self) -> str:
#     text = ''
#     if 'lognormal' in self.results:
#         text += r'$skew_{lognormal}$: ' + str(round(self.results['lognormal']['skew'], 2)) + '\n'
#         text += r'$pos_{lognormal}$: ' + str(format(self.results['lognormal']['pos'], '.2e')) + '\n'
#     if 'inv gamma' in self.results:
#         text += r'$a_{inv gamma}$: ' + str(round(self.results['inv gamma']['a'], 2)) + '\n'
#         text += r'$pos_{inv gamma}$: ' + str(format(self.results['inv gamma']['pos'], '.2e')) + '\n'
#     if 'alpha' in self.results:
#         text += r'$\alpha_{lognormal}$: ' + str(round(self.results['alpha'], 2)) + '\n'
#     if 'beta' in self.results:
#         text += r'$\beta_{lognormal}$: ' + str(round(self.results['beta'], 2)) + '\n'
#     if 'alpha gamma' in self.results:
#         text += r'$\alpha_{gamma}$: ' + str(round(self.results['alpha gamma'], 2)) + '\n'
#     if 'beta gamma' in self.results:
#         text += r'$\beta_{gamma}$: ' + str(round(self.results['beta gamma'], 2)) + '\n'
#     return text.strip('\n')
#
#
# def _label_error(self) -> str:
#     text = ''
#     for func, ress in self.results.items():
#         text += f'{func}: {ress["standard div"]:.2f}\n'
#     return text.strip('\n')
#
#
# def plot(self, functions: List[str], errors: bool, save: bool = False):
#     norm_I_hist(np.array(self.data.df), bins=100)
#     plt.title(f'Histogram and Probs of {self.data}')
#     plt.xlabel(r'$I_{norm}$')
#     plt.ylabel(r'$p(I)$')
#     text = self._label_error() if errors else self._label()
#     props = dict(boxstyle='round', facecolor='white')
#     plt.legend()
#     self.ax.text(0.6, 0.7, text, fontsize=12, verticalalignment='top', transform=self.ax.transAxes, bbox=props)
#     if save:
#         dir = f"Plots/{'_'.join(functions)}{'_errors' if errors else None}"
#         if not path.exists(dir):
#             os.makedirs(dir)
#         plt.savefig(f"{dir}/set{self.data.data_set}_{self.data.mode_rep}.pdf")
#     else:
#         plt.show()
#
#
# def calc_sigma(self, res: int = 101, plot: bool = False, **unused):
#     result = estimate_sigma(np.array(self.data.df), self.data.w_0, False, res, plot)
#     self.results['sigma'] = result[0]
#     self.results['beta'] = result[1]
#     self.results['standard div'] = result[-1]
#     return self.results
#
#
# def calc_sigma_gamma(self, res: int = 101, plot: bool = False, **unused):
#     result = estimate_sigma(np.array(self.data.df), self.data.w_0, True, res, plot)
#     self.results['sigma gamma'] = result[0]
#     self.results['beta gamma'] = result[1]
#     self.results['standard div gamma'] = result[-1]
#     return self.results
