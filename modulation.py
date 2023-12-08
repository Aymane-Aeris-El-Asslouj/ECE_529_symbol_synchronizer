import numpy as np


class DBPSKModulator:
    @staticmethod
    def modulate(data):
        return np.cumprod(1 - 2 * data)

    @staticmethod
    def demodulate(symbols):
        return (np.abs(symbols[1:] - symbols[:-1]) > 0.5).astype(int)
