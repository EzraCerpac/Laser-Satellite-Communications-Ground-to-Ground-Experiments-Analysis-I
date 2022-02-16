"""EQ's from Optimum divergence angle of a Gaussian beam wave in the presence of random jitter
in free-space laser communication systems p.570"""

def F_T(beta, P_F):
    """Fade level"""
    return (beta + 1) / beta * P_F ** (1 / beta)


def P_F(beta, I_F):
    """The desired fade probability at the tracking sensor"""
    return I_F ** beta


def S_T(beta, P_S):
    """Surge level"""
    return (beta + 1) / beta * (1-P_S) ** (1 / beta)


def P_S(beta, I_F):
    """The desired fade probability at the tracking sensor"""
    return (1-I_F) ** beta


def D(S_T, F_T):
    """Dynamic range required, just from angular jitter"""
    return S_T/F_T