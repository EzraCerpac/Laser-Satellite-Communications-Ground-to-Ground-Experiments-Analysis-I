# Random
import pandas as pd
from scipy.stats import beta

# Parameters
w_0 = 10
sigma = 2

# constant
beta0 = w_0 ** 2 / (4 * sigma ** 2)
# scale1 = 1/beta1
a0, b0 = beta0, 1

size = 10000
sample = pd.DataFrame(beta.rvs(a0, b0, size=size), columns=["intensity"])
