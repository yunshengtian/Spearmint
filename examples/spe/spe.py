import numpy as np

def main(job_id, params):
    x1 = params['x1']
    x2 = params['x2']
    x3 = np.round(params['x3'])  # Rounding x3 to the nearest integer as specified
    x4 = params['x4']
    x5 = params['x5']
    x6 = params['x6']
    x7 = params['x7']
    
    # Clipping x3 to its specified bounds [17, 28]
    x3 = np.clip(x3, 17, 28)
    
    # Objective function calculation
    f = 0.7854 * x1 * x2**2 * (3.3333 * x3**2 + 14.9334 * x3 - 43.0934) - 1.508 * x1 * (x6**2 + x7**2) + 7.4777 * (x6**3 + x7**3) + 0.7854 * (x4 * x6**2 + x5 * x7**2)
    
    # Constraints
    cons = np.array([
        1 - 27 * x1**(-1) * x2**(-2) * x3**(-1),
        1 - 397.5 * x1**(-1) * x2**(-2) * x3**(-2),
        1 - 1.93 * x2**(-1) * x3**(-1) * x4**(-3) * x6**(-4),
        1 - 1.93 * x2**(-1) * x3**(-1) * x5**(-3) * x7**(-4),
        1100 - ((745 * x4 / (x2 * x3))**2 + 16.9 * 10**6)**0.5 / (0.1 * x6**3),
        850 - ((745 * x5 / (x2 * x3))**2 + 157.5 * 10**6)**0.5 / (0.1 * x7**3),
        40 - x2 * x3,
        x1 / x2 - 5,
        12 - x1 / x2,
        1 - (1.5 * x6 + 1.9) / x4,
        1 - (1.1 * x7 + 1.9) / x5
    ])
    
    # Convert constraints into a single check; all must be >= 0
    c = float(np.all(cons >= 0)) - 0.5

    return {'f': f, 'c': c}

def true_val():
    return 2996.3482

def true_sol():
    return {'x1': 3.5, 'x2': 0.7, 'x3': 17, 'x4': 7.3, 'x5': 7.8, 'x6': 3.350215, 'x7': 5.286683}

true_func = main
