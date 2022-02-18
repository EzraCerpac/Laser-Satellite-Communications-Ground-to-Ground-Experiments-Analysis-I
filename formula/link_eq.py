from sympy import *

from formula.power_penalty import *

labda, R, A_r = symbols('lambda R A_r')

G_t = 8 / w_0 ** 2
L_r = (labda / (4 * pi * R)) ** 2
G_r = 4 * pi * A_r / labda ** 2
t_j = w_0 ** 2 / (4 * sigma ** 2 + w_0 ** 2)


P_t, tau_t, tau_r = symbols('P_t tau_t tau_r')

make_one = [P_t, tau_t, tau_r, A_r, R]
replacements = [(x, 1) for x in make_one] + [(a, 10*-4), (w_sigma, 20)]

P_r = P_t * tau_t * G_t * L_r * G_r * tau_r * t_j * L_j

pprint(P_r.subs(replacements))
