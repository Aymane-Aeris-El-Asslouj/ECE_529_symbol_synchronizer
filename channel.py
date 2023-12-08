import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import convolve
import scipy.signal as signal

from utils import plot_fft


class Channel:

    def __init__(self, channel_empty_duration, samples_per_symbol, symbol_delay, noise_level):

        self.channel_empty_duration = channel_empty_duration
        self.samples_per_symbol = samples_per_symbol
        self.symbol_delay = symbol_delay
        self.noise_level = noise_level

    def process(self, channel_input):

        pre_zeros = np.zeros((self.channel_empty_duration * self.samples_per_symbol,))
        post_zeros = np.zeros((self.channel_empty_duration * self.samples_per_symbol,))
        tx_concat = np.concatenate([pre_zeros, channel_input, post_zeros], axis=0)

        delayed_signal = self.apply_fractional_delay(tx_concat, self.samples_per_symbol * self.symbol_delay,
                                                     self.samples_per_symbol*10)

        filtered_white_gaussian = self.generate_filtered_noise(len(delayed_signal), self.noise_level)

        return tx_concat, delayed_signal, filtered_white_gaussian, delayed_signal + filtered_white_gaussian

    @staticmethod
    def apply_fractional_delay(signal, delay, filter_length=31):
        """
        Apply a fractional delay to a signal.

        :param signal: The input signal to be delayed.
        :param delay: The desired fractional delay (in samples).
        :param filter_length: The length of the filter (number of taps).
        :return: Delayed signal.
        """
        # Create an array of filter tap indices
        taps = np.arange(filter_length) - (filter_length - 1) / 2

        # Sinc function for the fractional delay filter
        h = np.sinc(taps - delay)

        # Apply a window function (like Hamming) to the filter coefficients
        h *= np.hamming(filter_length)

        # Normalize the filter coefficients
        h /= np.sum(h)

        # Apply the filter to introduce the delay
        return convolve(signal, h, mode='same')

    @staticmethod
    def generate_filtered_noise(num_samples, std_dev):
        """
        Generate white Gaussian noise, multiply it by a cosine wave, and apply a low-pass filter.

        Parameters:
        duration (float): Duration of the signal in seconds.
        fs (int): Sampling frequency in Hz.
        std_dev (float): Standard deviation of the Gaussian noise.
        omega (float): Frequency of the cosine wave in radians/sec.
        cutoff (float): Cutoff frequency of the low-pass filter in Hz.

        Returns:
        np.ndarray: Array containing the filtered noise signal.
        """
        # Generate white Gaussian noise
        noise = np.random.normal(0, std_dev, num_samples*1000)

        # Multiply noise by cosine wave
        modulated_noise = noise * np.cos(np.pi * np.arange(0, num_samples, 1 / 1000))

        # Design low-pass filter
        cutoff = 1/20
        order = 5
        b, a = signal.butter(order, cutoff, btype='low', analog=False, output='ba')

        # Apply low-pass filter
        filtered_signal = signal.filtfilt(b, a, modulated_noise)

        return filtered_signal[::1000]