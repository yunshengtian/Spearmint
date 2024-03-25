import numpy as np

def main(job_id, params):
    x1 = params['x1']
    x2 = params['x2']
    x3 = params['x3']
    x4 = params['x4']
    
    # Objective function
    f = 1.10471 * x1**2 * x2 + 0.04811 * x3 * x4 * (14.0 + x2)
    
    # Constraints
    tau1 = 6000.0 / (np.sqrt(2) * x1 * x2)
    tau2 = 6000 * (14 + 0.5 * x2) * np.sqrt(0.25 * (x2**2 + (x1 + x3)**2)) / \
        (2 * 0.707 * x1 * x2 * (x2**2 / 12 + 0.25 * (x1 + x3)**2))
    tau = np.sqrt(tau1**2 + tau2**2 + x2 * tau1 * tau2 / np.sqrt(0.25 * (x2**2 + (x1 + x3)**2)))
    sigma = 504000.0 / (x3**2 * x4)
    P_c = 64746.022 * (1 - 0.0282346 * x3) * x3 * x4**3
    delta = 2.1952 / (x3**3 * x4)
    
    # Constraint checks
    c1 = 13000 - tau
    c2 = 30000 - sigma
    c3 = x4 - x1
    c4 = P_c - 6000
    c5 = 0.25 - delta
    
    # Combine constraints
    c = float(c1 >= 0 and c2 >= 0 and c3 >= 0 and c4 >= 0 and c5 >= 0) - 0.5

    return {'f': f, 'c': c}

def true_val():
    return 2.381065

def true_sol():
    return {'x1': 0.24435257, 'x2': 6.2157922, 'x3': 8.2939046, 'x4': 0.24435258}

true_func = main
