import numpy as np

def main(job_id, params):
  x1 = params['x1']
  x2 = params['x2']

  f  = x1 + x2
  c1 = x1 + 2.0*x2 + 0.5*np.sin(2*np.pi*(x1**2 - 2.0*x2)) - 1.5
  c2 = 1.5 - x1**2 - x2**2

  c = (c1 >= 0 and c2 >= 0).astype(float) - 0.5

  return {'f':f, 'c': c}

def true_val():
    return 0.5998
def true_sol():
    return {'x1' : 0.1954, 'x2' : 0.4044}
true_func = main    
