import numpy as np

def main(job_id, params):
    x1 = params['x1']
    x2 = params['x2']
    x3 = params['x3']
    x4 = params['x4']
    
    # Objective function calculation
    f = 861000 * x1**(0.5) * x2 * x3**(-2/3) * x4**(-0.5) + 36900 * x3 + 772000000 * x1**(-1) * x2**(0.219) - 765430000 * x1**(-1)
    
    # Constraint
    cons = x4 * x2**(-2) + x2**(-2) - 1
    # Constraint check; converting to the desired format where -0.5 indicates failure and 0.5 indicates success
    c = float(-cons >= 0) - 0.5

    return {'f': f, 'c': c}

def true_val():
    return 2964895.417339161

def true_sol():
    return {'x1': 49.99999999999584, 'x2': 1.178283949974269, 'x3': 24.592589925270623, 'x4': 0.3883530667669658}

true_func = main
