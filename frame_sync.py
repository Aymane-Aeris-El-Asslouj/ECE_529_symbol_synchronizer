import numpy as np
from utils import *

class FrameSync:

    def __init__(self, pre_preamble, preamble, frame_data_size):

        self.pre_preamble = pre_preamble
        self.preamble = preamble
        self.frame_data_size = frame_data_size


    def frame_bits(self, bits):
        """
        Generates a numpy array that starts with alternating 1 and -1, then at indices i,
        it adds the preamble followed by the user-provided string encoded in bits.

        :param data_string: The user-provided string to encode in the array.
        :return: The generated numpy array.
        """
        return np.concatenate([self.pre_preamble, self.preamble, bits], axis=0)

    def unframe_data(self, framed_data):
        """
        Finds the starting indices of the specified sequence in an array of 1's and 0's.

        :param arr: List of 1's and 0's.
        :param sequence: The sequence to find in arr.
        :return: List of starting indices where the sequence is found.
        """
        preamble_length = len(self.preamble)
        # Iterate over the array
        for preamble_index in range(len(framed_data) - preamble_length - self.frame_data_size + 1):
            if all( a == b for a, b in zip(framed_data[preamble_index:preamble_index + preamble_length], self.preamble)):
                data_start = preamble_index + preamble_length
                string_bits = framed_data[data_start:data_start+self.frame_data_size]
                return preamble_index, bits_to_string(string_bits)
        return None, None