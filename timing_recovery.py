from typing import List

import numpy as np

from utils import *


class SymbolSynchronizer:

    def __init__(self, sync_type, loop_gain):
        self.sync_type = sync_type
        self.loop_gain = loop_gain

    def process(self, samples: List[complex], samples_per_symbol):

        in_index = 0
        sps = samples_per_symbol
        tau = 0 # phase error in samples

        output_x = np.zeros_like(samples)

        output_list = []
        j = 0
        while in_index + 2*sps < len(samples):
            x_1 = samples[in_index + 0 * sps + 0 * int(sps/2)]
            x_12 = samples[in_index + 0 * sps + 1 * int(sps/2)]
            x_pre2 = samples[in_index + 1 * sps + 0 * int(sps/2) - 1]
            x_2 = samples[in_index + 1 * sps + 0 * int(sps/2)]
            x_post2 = samples[in_index + 1 * sps + 0 * int(sps/2) + 1]
            x_23 = samples[in_index + 1 * sps + 1 * int(sps/2)]
            x_3 = samples[in_index + 2 * sps + 0 * int(sps/2)]

            # estimated_optimal_sample
            output_list.insert(0, x_2)
            output_x[in_index + 1 * sps + 0 * int(sps/2)] = 1 #####

            timing_error = 0
            if self.sync_type == "gardner":
                timing_error = x_2.real * (x_12.real - x_23.real)
            elif self.sync_type == "MM":
                timing_error = x_2.real * sng(x_1.real) - x_1 * sng(x_2.real)
            elif self.sync_type == "EL":
                timing_error = -sps * sng(x_2) * (x_post2 - x_pre2)/2
            else:
                print("WHAT")
                exit()

            new_tau = tau - timing_error * self.loop_gain
            in_index += int(sps + (np.floor(new_tau) - np.floor(tau)))
            tau = new_tau

            j+=1

        output_list.reverse()
        return output_x, np.array(output_list)