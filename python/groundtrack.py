import numpy as np
from typing import Tuple

a_k = 6378137
a = 6371000
e2 = 0.00669438002290


def hirvonen(x: float, y: float, z: float) -> Tuple[np.ndarray, np.ndarray, float]:
    eps = np.deg2rad(0.00005 / 60**2)
    r = np.sqrt(x * x + y * y)
    phi = np.arctan(z / (r * (1 - e2)))
    while 1:
        N = a / np.sqrt(1 - e2 * np.sin(phi) ** 2)
        h = r / np.cos(phi) - N
        new_phi = np.arctan(z / r / (1 - e2 * (N / (N + h))))
        if abs(new_phi - phi) < eps:
            phi = new_phi
            break
        else:
            phi = new_phi

    lam = np.arctan2(y, x)
    return np.degrees(phi), np.degrees(lam), h
