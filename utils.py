import numpy as np
import matplotlib.pyplot as plt

def generate_data(data_size_):
    return np.random.randint(0, 2, data_size_)

def string_to_bits(text):
    return [int(bit) for char in text for bit in format(ord(char), '08b')]

def bits_to_string(bits):
    string = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        byte_string = ''.join(str(bit) for bit in byte)
        string.append(chr(int(byte_string, 2)))
    return string

def calculate_ber(tx_string, rx_string):

    if rx_string is None:
        return 1

    tx_bits, rx_bits = string_to_bits(tx_string), string_to_bits(rx_string)

    return sum(a != b for a, b in zip(tx_bits, rx_bits))/len(tx_bits)

def plot_complex_samples(samples, title="Complex IQ Samples"):
    """
    Plots a list of complex IQ samples.

    Args:
    samples (list of complex): List of complex IQ samples.
    title (str): Title for the plot (optional).
    """
    plt.figure(figsize=(10, 6))
    plt.plot(samples.real, samples.imag, 'b.')
    plt.title(title)
    plt.xlabel('In-Phase (I)')
    plt.ylabel('Quadrature (Q)')
    plt.grid(True)
    plt.show()

def apply_constant_phase_shift(samples, phase_shift):
    return samples * np.exp(1j * phase_shift)


def time_plot_complex_samples(signal, title="Complex IQ Samples"):
    plt.figure()
    plt.plot(np.real(signal), label='I (Real) Component')
    plt.plot(np.imag(signal), label='Q (Imaginary) Component')
    plt.title(title)
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

def upsample(signal, factor):
    """
    Manually upsample a signal by inserting zeros between samples.

    :param signal: The input signal (1-D numpy array).
    :param factor: Upsampling factor (integer).
    :return: Upsampled signal.
    """
    upsampled_length = len(signal) * factor
    upsampled_signal = np.zeros(upsampled_length)
    upsampled_signal[::factor] = signal
    return upsampled_signal

def downsample(signal, factor):
    """
    Manually downsample a signal by selecting every Nth sample.

    :param signal: The input signal (1-D numpy array).
    :param factor: Downsampling factor (integer).
    :return: Downsampled signal.
    """
    return signal[::factor]

def plot_fft(signals, names, fs):
    """
    Plots the Fast Fourier Transforms (FFTs) of multiple signals on the same graph.

    Parameters:
    signals (list of np.ndarray): List of signal arrays.
    names (list of str): List of names for each signal.
    fs (float): Sampling frequency of the signals in Hz.
    """
    plt.figure(figsize=(12, 6))

    for i, signal in enumerate(signals):
        # Compute the FFT
        fft_result = np.fft.fft(signal)

        # Compute the frequency bins
        freq = np.fft.fftfreq(len(signal), 1/fs)

        # Compute the magnitude spectrum
        magnitude = np.abs(fft_result)

        # Plotting
        plt.plot(freq, magnitude, label=names[i])

    plt.title('FFT of noise')
    plt.xlabel('Digital as a fraction of pi')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.legend()
    plt.xlim(0, fs/2)

    plt.show()


def sng(num):
    """
    Returns the sign of a given number as an integer.
    -1 for negative numbers, 1 for positive numbers, 0 for zero.
    """
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0

