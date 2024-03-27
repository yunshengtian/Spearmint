import numpy as np

P = 50e3  # Load in Newtons
E = 200e9  # Young's modulus in Pascals
sigma_allow = 35e7  # Allowable stress in Pascals
AR = 25  # Aspect ratio
L_min = 6  # Minimum total length
d = 10  # Number of sections

def evaluate_true(X):
    delta = 0
    for i in range(1, d + 1):
        bi = X[i - 1]  # b_i
        hi = X[10 + i - 1]  # h_i
        li = X[20 + i - 1]  # l_i

        # Sums of lengths from i to d
        sum1 = X[20 + i - 1:].sum() if i <= d else 0
        sum2 = X[20 + i:].sum() if i < d else 0

        bracket_term = (12 / (bi * hi**3)) * (sum1**3 - sum2**3)
        delta += bracket_term

    f = P * delta / (3 * E)
    return f

def evaluate_slack_true(X):
    cons = np.zeros(21)
    sum_l = 0
    for i in range(1, d + 1):
        bi = X[i - 1]
        hi = X[10 + i - 1]
        li = X[20 + i - 1]

        sum_lj = X[20 + i - 1:].sum() if i <= d else 0
        
        cons[i - 1] = (6 * P * sum_lj) / (bi * hi**2) - sigma_allow  # Bending stress constraint
        cons[10 + i - 1] = hi/bi - AR  # Aspect ratio constraint
        sum_l += li

    cons[-1] = L_min - sum_l  # Minimum length constraint
    return cons

def main(job_id, params):
    X_b = params['b']
    X_h = params['h']
    X_l = params['l']
    X = np.concatenate((X_b, X_h, X_l))

    f = evaluate_true(X)
    cons = evaluate_slack_true(X)
    # Constraint satisfaction check
    c = np.all(cons <= 0, axis=0).astype(float) - 0.5
    return {'f': f, 'c': c}
