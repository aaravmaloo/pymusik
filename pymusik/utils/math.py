import numpy as np

def linear_to_db(linear: float) -> float:
    return 20 * np.log10(np.maximum(linear, 1e-12))

def db_to_linear(db: float) -> float:
    return 10 ** (db / 20)

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def clamp(val: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(val, max_val))
