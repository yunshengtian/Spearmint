import numpy as np

l = 100
P = 2
sigma = 2

def evaluate_true(x1, x2):
    f = l * (x2 + 2 * np.sqrt(2) * x1)
    return f

def evaluate_slack_true(x1, x2):
    cons = np.array([
        -x2 / (2 * x2 * x1 + np.sqrt(2) * x1**2) * P + sigma,
        -(x2 + np.sqrt(2) * x1) / (2 * x2 * x1 + np.sqrt(2) * x1**2) * P + sigma,
        -1 / (x1 + np.sqrt(2) * x2) * P + sigma,
    ])
    return cons

def main(job_id, params):
    x1 = params['x1']
    x2 = params['x2']
    
    f = evaluate_true(x1, x2)
    cons = evaluate_slack_true(x1, x2)
    
    # Constraint check; converting to the desired format
    c = float(np.all(cons <= 0)) - 0.5

    return {'f': f, 'c': c}
