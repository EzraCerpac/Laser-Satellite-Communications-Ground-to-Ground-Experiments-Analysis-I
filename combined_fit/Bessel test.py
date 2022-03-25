import math

import pandas.plotting
from scipy import special
from combined_fit.I_0_calc import main
from combined_fit.indices import rytov_index
from formula.jitter import k
import numpy as np
import pandas as pd
import matplotlib as plt
from combined_fit.angular_jitter_fit_gamma import alphafun
from combined_fit.angular_jitter_fit_gamma import betafun
from matplotlib import pyplot as plt
from combined_fit.scintillation import integrate_scint_index
from formula.normalize import norm_I

Cn = pd.read_pickle('../Data/DFs/Cn.pickle')
I = np.array(pd.read_pickle('../Data/DFs/data18/off1.pickle'))
#scint_index = integrate_scint_index(I, )
II = norm_I(I, True)
alpha  = alphafun()
beta = betafun()
print(alpha, beta)
bessellist = np.empty(0)
xlist = np.empty(0)
thinglist = np.empty(0)
arglist = np.empty(0)
for i in range(II.shape[0]):
    x = 2 * math.sqrt(alpha * beta * II[i])
    bessel = special.kv(alpha - beta, 2 * math.sqrt(alpha * beta * II[i]))
    xlist = np.append(xlist, x)
    bessellist = np.append(bessellist, bessel)
    gammathing = ((2 * (alpha * beta) ** ((alpha + beta) / 2 )) / (special.gamma(alpha) * special.gamma(beta) * II[i])) * ((II[i]) ** ((alpha + beta) / 2))
    thinglist = np.append(thinglist, gammathing)
    arg = 2 * math.sqrt(alpha * beta * II[i])
    arglist = np.append(arglist, arg)
plt.plot(II, thinglist, color='r')
plt.title('thing')
plt.xlabel('x')
plt.ylabel('thing')
#plt.xlim((0,0.05))
plt.show()

plt.plot(II, bessellist, color='r')
plt.title('Bessel')
plt.xlabel('x')
plt.ylabel('Bessel')
#plt.xlim((0,0.05))
plt.show()

plt.plot(II, arglist, color='r')
plt.title('Bessel')
plt.xlabel('x')
plt.ylabel('Bessel')
#plt.xlim((0,0.05))
plt.show()

plt.hist(norm_I(I,False), bins='auto')
plt.show()