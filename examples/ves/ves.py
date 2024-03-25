import numpy as np

def evaluate_true(x1, x2, x3, x4):
    f = 0.6224 * x1 * x3 * x4 + 1.7781 * x2 * x3**2 + 3.1661 * x1**2 * x4 + 19.84 * x1**2 * x4
    return f

def evaluate_slack_true(x1, x2, x3, x4):
    con1 = x1 - 0.0193 * x3
    con2 = x2 - 0.00954 * x3
    con3 = np.pi * x3**2 * x4 + (4/3) * np.pi * x3**3 - 1296000
    con4 = 240 - x4
    cons = np.array([con1, con2, con3, con4])
    return cons

def main(job_id, params):
    x1 = params['x1']
    x2 = params['x2']
    x3 = params['x3']
    x4 = params['x4']
    
    f = evaluate_true(x1, x2, x3, x4)
    cons = evaluate_slack_true(x1, x2, x3, x4)
    
    # Constraint check; converting to the desired format
    c = float(np.all(cons <= 0)) - 0.5

    return {'f': f, 'c': c}
