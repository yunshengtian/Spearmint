import numpy as np

# Helper function for safe division
def safe_divide(x1, x2):
    if np.isscalar(x1):
        x1 = np.array([x1])
    return np.divide(x1, x2, out=np.zeros_like(x1, dtype=float), where=x2!=0)

i01 = 3.11
i02 = 1.84
i0r = -3.11
dmax = 220
eps = 0.5

def evaluate_true(X):
    n1, n2, n3, n4, n5, n6, p, m1, m2 = X
    n1 = np.clip(np.round(n1), 17, 110)
    n2 = np.clip(np.round(n2), 14, 58)
    n3 = np.clip(np.round(n3), 14, 46)
    n4 = np.clip(np.round(n4), 17, 104)
    n5 = np.clip(np.round(n5), 14, 46)
    n6 = np.clip(np.round(n6), 25, 200)
    p = np.clip(np.round(p), 3, 5)
    m1 = np.round(m1 * 4) / 4.0
    m2 = np.round(m2 * 4) / 4.0

    i1 = safe_divide(n6, n4)
    i2 = safe_divide(n6 * (n1 * n3 + n2 * n4), n1 * n3 * (n6 - n4))
    ir = safe_divide(n2 * n6, n1 * n3)
    f = np.max(np.array([np.abs(i1 - i01), np.abs(i2 - i02), np.abs(ir - i0r)]), axis=0)
    
    return f

def evaluate_slack_true(X):
    n1, n2, n3, n4, n5, n6, p, m1, m2 = X
    n1 = np.clip(np.round(n1), 17, 110)
    n2 = np.clip(np.round(n2), 14, 58)
    n3 = np.clip(np.round(n3), 14, 46)
    n4 = np.clip(np.round(n4), 17, 104)
    n5 = np.clip(np.round(n5), 14, 46)
    n6 = np.clip(np.round(n6), 25, 200)
    p = np.clip(np.round(p), 3, 5)
    m1 = np.round(m1 * 4) / 4.0
    m2 = np.round(m2 * 4) / 4.0

    # Constraints computations
    beta = np.arccos(np.clip(safe_divide((n6 - n3)**2 + (n4 + n5)**2 - (n3 + n5)**2, 2 * (n6 - n3) * (n4 + n5)), -1, 1))
    c1 = m2 * (n6 + 2.5) - dmax
    c2 = m1 * (n1 + n2) + m1 * (n2 + 2) - dmax
    c3 = m2 * (n4 + n5) + m2 * (n5 + 2) - dmax
    c4 = np.abs(m1 * (n1 + n2) - m2 * (n6 - n3)) - m1 - m2
    c4 = - ((n1 + n2) * np.sin(safe_divide(np.pi, p)) - n2 -2 - eps)
    c5 = - ((n6 - n3) * np.sin(safe_divide(np.pi, p)) - n3 -2 - eps)
    c6 = - ((n4 + n5) * np.sin(safe_divide(np.pi, p)) - n5 -2 - eps)
    c7 = - ((n6 - n3)**2 + (n4 + n5)**2 - 2 * (n6 - n3) * (n4 + n5) * np.cos(safe_divide(2 * np.pi, p) - beta) - (n3 + n5 + 2 + eps)**2)
    c8 = - (n6 - 2 * n3 - n4 - 4 - 2 * eps)
    c9 = - (n6 - n4 - 2 * n5 - 4 - 2 * eps)
    cons = np.array([c1, c2, c3, c4, c5, c6, c7, c8, c9])  # Update with the correct constraint calculations
    
    return cons

def main(job_id, params):
    X = np.array([params['n1'], params['n2'], params['n3'], params['n4'], params['n5'], params['n6'], params['p'], params['m1'], params['m2']])
    f = evaluate_true(X)
    cons = evaluate_slack_true(X)
    
    c = np.all(cons <= 0, axis=0).astype(float) - 0.5

    return {'f': f, 'c': c}
