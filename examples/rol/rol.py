import numpy as np
import math

D = 160
d = 90
Bw = 30

def _calc_fc(Db, Dm, fi, fo):
    gamma = Db / Dm
    fc = 37.91 * (1 + (1.04 * ((1 - gamma) / (1 + gamma)) ** 1.72 * ((fi * (2 * fo - 1)) / (fo * (2 * fi - 1))) ** 0.41) ** (10 / 3)) ** -0.3 * \
        ((gamma ** 0.3 * (1 - gamma) ** 1.39) / (1 + gamma) ** (1 / 3)) * (2 * fi / (2 * fi - 1)) ** 0.41
    return fc

def _calc_phi0(Db):
    T = D - d - 2 * Db
    phi0 = 2 * math.pi - 2 * np.arccos(
        (((D - d) / 2 - 3 * (T / 4)) ** 2 + (D / 2 - T / 4 - Db) ** 2 - (d / 2 + T / 4) ** 2) /
        (2 * ((D - d) / 2 - 3 * (T / 4)) * (D / 2 - (T / 4) - Db))
    )
    return phi0

def main(job_id, params):
    Dm, Db, Z, fi, fo, KDmin, KDmax, eps, e, xi = params['Dm'], params['Db'], params['Z'], params['fi'], params['fo'], params['KDmin'], params['KDmax'], params['eps'], params['e'], params['xi']
    
    fc = _calc_fc(Db, Dm, fi, fo)
    case_1 = Db <= 25.4
    Cd = np.zeros_like(Db)
    Cd[case_1] = (fc * Z ** (2 / 3) * Db ** 1.8)[case_1]
    Cd[~case_1] = (3.647 * fc * Z ** (2 / 3) * Db ** 1.4)[~case_1]
    objective = -Cd
    
    phi0 = _calc_phi0(Db)
    cons = -np.array([
        Z - phi0 / (2 * np.arcsin(Db / Dm)) - 1,
        KDmin * (D - d) - 2 * Db,
        2 * Db - KDmax * (D - d),
        xi * Bw - Db,
        0.5 * (D + d) - Dm,
        Dm - (0.5 + e) * (D + d),
        eps * Db - 0.5 * (D - Dm - Db),
    ])
    
    c = float(np.all(cons >= 0)) - 0.5

    return {'f': objective, 'c': c}

