import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import norm, rv_continuous, beta

# %%
# Random
w_0 = 10
sigma = 2

# constant
beta0 = w_0 ** 2 / (4 * sigma ** 2)
# scale1 = 1/beta1
a0, b0 = beta0, 1
# %%
size = 1000000
sample = pd.DataFrame(beta.rvs(a0, b0, size=size), columns=["intensity"])
# %%

# plt.show()
# %%
sample_mean = sample['intensity'].mean()
sample_std = sample['intensity'].std()
print(f'{sample_mean = }, and {sample_std = }')
# %%
dist = norm(sample_mean, sample_std)
dist_params = rv_continuous.fit(sample.intensity)
print(dist_params)
# %%
sample.plot(kind='hist', label='sample intensity', density=True)
# I = np.linspace(beta.ppf(0.01, a, b), beta.ppf(0.99, a, b), 101)
I = np.linspace(0, 1, 101)
plt.plot(I, beta.pdf(I, a0, b0), 'r-', label='beta pdf')
plt.legend()
plt.show()
# %%
a1, b1, loc1, scale1 = beta.fit(sample.intensity, fb=1, floc=0, fscale=1)
beta1 = a1
sigma1 = np.sqrt(w_0 ** 2 / (4 * beta1))
print(sigma1)
# %%
