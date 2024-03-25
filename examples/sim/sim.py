import numpy as np

def evaluate_true(x1, x2):
    f = 0.1 * x1 * x2
    return f

def evaluate_slack_true(x1, x2):
    rt, rs, n = 1, 0.2, 8
    # Ensure non-zero denominator for arctan calculation
    x2_safe = np.where(x2 == 0, 1e-10, x2)
    cons = (rt + rs * np.cos(n * np.arctan(x1 / x2_safe))) ** 2 - x1 ** 2 - x2 ** 2
    return cons

def main(job_id, params):
    x1 = params['x1']
    x2 = params['x2']
    
    f = evaluate_true(x1, x2)
    cons = evaluate_slack_true(x1, x2)
    
    # Constraint check; converting to the desired format
    c = float(cons >= 0) - 0.5

    return {'f': f, 'c': c}
