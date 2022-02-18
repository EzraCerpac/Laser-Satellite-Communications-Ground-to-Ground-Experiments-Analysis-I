from sympy import *

a, Q, Q_r, w_0, sigma, I = symbols('a Q Q_r w_0 sigma I')

BER = 1 / 2 * erfc(Q / sqrt(2))

w_sigma = w_0 / sigma

beta = w_sigma**2/4

average_BER = Q_r*(beta+1)/2 * Integral(I ** (beta - 1) * erfc(I * Q_r * (beta + 1) / (sqrt(2) * beta)), (I, 0, 1))

L_j = solve(BER - a, Q)[0] / solve(average_BER - a, Q_r)[0]

# pprint(solve(average_BER - a, Q_r)[0])
