import numpy as np

def evaluate_true(x1, x2):
    f = -np.cos((x1 - 0.1) * x2) ** 2 - x1 * np.sin(3 * x1 + x2)
    return f

def evaluate_slack_true(x1, x2):
    t = np.arctan2(x1, x2)
    cons = (2 * np.cos(t) - 0.5 * np.cos(2 * t) - 0.25 * np.cos(3 * t) - 0.125 * np.cos(4 * t)) ** 2 + (2 * np.sin(t)) ** 2 - x1 ** 2 - x2 ** 2
    return cons

def main(job_id, params):
    x1 = params['x1']
    x2 = params['x2']
    
    f = evaluate_true(x1, x2)
    cons = evaluate_slack_true(x1, x2)
    
    # Constraint check; -0.5 indicates failure, 0.5 indicates success
    c = float(cons >= 0) - 0.5

    return {'f': f, 'c': c}
