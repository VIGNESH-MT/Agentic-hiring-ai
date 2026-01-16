# src/analytics/stats_utils.py
import numpy as np

def safe_variance(values):
    """
    Staff-level guard against degenerate statistical inputs.
    """
    if values is None or len(values) < 2:
        return 0.0
    return float(np.var(values))


def safe_covariance(x, y):
    """
    Safe covariance for low-sample interactive systems.
    """
    if x is None or y is None or len(x) < 2 or len(y) < 2:
        return 0.0
    return float(np.cov(x, y)[0, 1])
