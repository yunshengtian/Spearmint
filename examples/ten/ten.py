import numpy as np

def main(job_id, params):
    x1 = np.round(params['x1'])  # Rounding x1 to the nearest integer value as specified
    x2 = params['x2']
    x3 = params['x3']
    
    # Clipping x1 to its specified bounds [2, 15]
    x1 = np.clip(x1, 2, 15)
    
    f = (x1 + 2) * x2 * x3**2
    
    # Constraints
    c1 = x2**3 * x1 / (71785 * x3**4) - 1
    c2 = 1 - (4 * x2**2 - x3 * x2) / (12566 * (x2 * x3**3 - x3**4)) - 1 / (5108 * x3**2)
    c3 = 140.45 * x3 / (x2**2 * x1) - 1
    c4 = 1 - (x2 + x3) / 1.5
    
    # Combine constraints into a single measure
    # This check passes if all constraints are >= 0
    c = float(c1 >= 0 and c2 >= 0 and c3 >= 0 and c4 >= 0) - 0.5

    return {'f': f, 'c': c}

def true_val():
    return 0.012666

def true_sol():
    # Return one of the optimizers as an example
    return {'x1': 11.329555, 'x2': 0.356032, 'x3': 0.051661}

true_func = main
