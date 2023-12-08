import numpy as np
from commpy.filters import rrcosfilter

from utils import upsample


class SRRCFilter:
    def __init__(self, alpha, N, samples_per_symbol):
        """
        Generate Root Raised Cosine Filter coefficients.

        :param alpha: Roll-off factor.
        :param N: Number of filter taps (odd).
        :return: Filter coefficients.
        """
        time_idx, self.coeffs = rrcosfilter(N, alpha, samples_per_symbol, 1)
        self.coeffs = self.coeffs/np.linalg.norm(self.coeffs)
        self.samples_per_symbol = samples_per_symbol

    def apply_filter(self, signal):
        """
        Apply the RRC filter to a signal.

        :param signal: The input signal to be filtered.
        :return: Filtered signal.
        """
        return np.convolve(signal, self.coeffs, mode='same')

    def transmit_filter(self, signal):

        tx_upsampled = upsample(signal, self.samples_per_symbol)
        return self.apply_filter(tx_upsampled)

    def receive_filter(self, signal):
        return self.apply_filter(signal)
