import numpy as np

def derivative_cdf(x):
    return 1 / np.sqrt(2 * np.pi) * np.exp(- x**2 / 2)