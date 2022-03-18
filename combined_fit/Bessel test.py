import math
from scipy import special
from combined_fit.I_0_calc import main
from combined_fit.indices import rytov_index
from formula.jitter import k
import numpy as np
import pandas as pd
from conf.config import FileConfig
alpha  = 0.1
beta = 0.9
I = np.array(pd.read_pickle('../Data/DFs/data18/off1.pickle'))
#for i in range(I.shape[0]):
    #bessel = special.kn(alpha - beta, 2 * math.sqrt(alpha * beta * I[i] / main()))
#print(bessel)

gamma = ((2 * (alpha * beta) ** ((alpha + beta) / 2)) / (special.gamma(alpha) * special.gamma(beta) * I[1000])) * ((I[1000] / main()) ** ((alpha + beta) / 2)) * special.kv(alpha, beta) * 2 * math.sqrt(alpha * beta * I[1000] / main())
print(gamma)
print(2 * math.sqrt(alpha * beta * I[1000]))
print(I[1000])
print(main())