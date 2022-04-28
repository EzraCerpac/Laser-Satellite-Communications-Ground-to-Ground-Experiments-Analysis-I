from __future__ import annotations

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import special

from combined_fit.indices import rytov_index
from formula.jitter import k
from formula.normalize import norm_I
from combined_fit.angular_jitter_fit_gamma import gamma_gamma
from combined_fit.angular_jitter_fit_beta import beta_func
from combined_fit.scintillation import probability_dist
from scipy import integrate
from combined_fit.indices import scintillation_index
from combined_fit.indices import rytov_index_const
from formula.jitter import k

Cn = pd.read_pickle('../Data/DFs/Cn.pickle')
I = [1,2,3]

labda = 1550e-9

print(integrate.quad(beta_func([1,2,3], 0.4) * probability_dist(
        0.5, 0.5, scintillation_index(rytov_index_const(
            k(labda), 0.4, 0.3
        ))), 0, 1))
