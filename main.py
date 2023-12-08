import matplotlib.pyplot as plt

from channel import *
from filters import *
from frame_sync import *
from timing_recovery import *
from utils import *
from modulation import *
import numpy as np

def compute_BER(sync_type, loop_gain, noise_level, symbol_delay):

    """Parameters"""

    "Source"
    TEST_STRING = "Hello World!"  # for bit error rate computation

    "Framing"
    PREPREAMBLE_BITS = [1] * 24  # for symbol timing synchronization
    PREAMBLE_BITS = string_to_bits(f'\xDB\x1A')  # for frame synchronization, bits: 1 1 0 1 1 0 1 1 0 0 0 1 1 0 1 0
    FRAME_DATA_SIZE = len(TEST_STRING)*8
    frame_sync = FrameSync(PREPREAMBLE_BITS, PREAMBLE_BITS, FRAME_DATA_SIZE)

    "Modulation"
    dbpsk_modulator = DBPSKModulator()

    "Timing synchronization"
    SYNCRONIZER_TYPE = sync_type
    LOOP_GAIN = loop_gain
    symbol_synchronizer = SymbolSynchronizer(SYNCRONIZER_TYPE, LOOP_GAIN)

    "Pulse shaping"
    SAMPLES_PER_SYMBOL = 16
    PULSE_TAP_COEFFIECIENTS_NUMBER = SAMPLES_PER_SYMBOL*10
    ROLL_OFF_FACTOR = 0.5
    srrc_filter = SRRCFilter(ROLL_OFF_FACTOR, PULSE_TAP_COEFFIECIENTS_NUMBER, SAMPLES_PER_SYMBOL)

    "Channel"
    CHANNEL_EMPTY_DURATION = 50  # allows to simulate the reaction of the receiver to an empty channel
    SYMBOL_DELAY = symbol_delay
    NOISE_LEVEL = noise_level
    channel = Channel(CHANNEL_EMPTY_DURATION, SAMPLES_PER_SYMBOL, SYMBOL_DELAY, NOISE_LEVEL)

    """Transmitter chain"""

    tx_source_bits = string_to_bits(TEST_STRING)
    tx_framed_bits = frame_sync.frame_bits(tx_source_bits)
    tx_modulated = dbpsk_modulator.modulate(tx_framed_bits)
    tx_filtered = srrc_filter.transmit_filter(tx_modulated)

    """Channel"""
    tx_concat, delayed_signal, filtered_white_gaussian, channel_output = channel.process(tx_filtered)

    """Receiver chain"""
    rx_filtered = srrc_filter.receive_filter(channel_output)
    trigger_history, rx_timing_recovered = symbol_synchronizer.process(rx_filtered, SAMPLES_PER_SYMBOL)
    rx_demodulated = dbpsk_modulator.demodulate(rx_timing_recovered)
    preamble_index, rx_data_unframed = frame_sync.unframe_data(framed_data=rx_demodulated)
    rx_data = rx_data_unframed

    """Testing"""
    BER = calculate_ber(TEST_STRING, rx_data)
    # print("Bit Error Rate (BER): ", BER)
    # print(rx_data)

    return BER




    # print(list(tx_modulated))
    # # formatted = [f"{x:.3f}" for x in list(tx_filtered)]
    # # for num in formatted:
    # #     print(num, end =', ')
    #
    # # print(output_x)
    # plt.figure()
    # plt.xlabel("Sample (n)")
    # plt.ylabel("Signal level")
    # plt.title("Optimal samples as determined by Early-Late Gate")
    # #plt.plot(tx_concat, label='tx_filtered')
    # #plt.plot(rx_filtered, label='rx_filtered')
    # plt.plot(trigger_history, label='optimal samples')
    # # plt.plot(filtered_white_gaussian, label="AWGN")
    # #plt.plot(channel_output, label="channel_output")
    # plt.plot(rx_filtered, label='receiver filtered')
    #
    # ind = 0
    # for idx, val in enumerate(trigger_history[:-SAMPLES_PER_SYMBOL*2]):
    #     if val == 1:
    #         plt.annotate(str(ind),  # The text to display str(ind) + "," +
    #                      (idx, val),  # The point (x,y) to annotate
    #                      textcoords="offset points",  # How to position the text
    #                      xytext=(0, 10),  # Distance from text to points (x,y)
    #                      ha='center')  # Horizontal alignment
    #
    #         if rx_data is not None:
    #             if preamble_index == ind:
    #                 plt.annotate("P1",  (idx, val), textcoords="offset points", xytext=(0, 15), ha='center', color='purple')
    #             if preamble_index + len(PREAMBLE_BITS) == ind:
    #                 plt.annotate("P2",  (idx, val), textcoords="offset points", xytext=(0, 15), ha='center', color='purple')
    #         ind += 1
    #
    #
    # #plt.scatter(list(range(len(tx_data))), tx_data, label='tx_data')
    # # plt.scatter(list(range(len(rx_timing_recovered))), rx_timing_recovered, label='rx_timing_recovered')
    # # plt.xlabel('Sample')
    # # plt.ylabel('Amplitude')
    #
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    #
    # time_plot_complex_samples(rx_filtered, title="a")
    # time_plot_complex_samples(rx_timing_recovered, title="a")

    #plot_complex_samples(tx_filter_sig, title="Complex IQ Samples")

if __name__ == "__main__":

    TEST_ITERATIONS = 50
    noise_levels =  np.arange(0, 2, 0.05)
    loop_gain = 0.3 #np.arange(0.1, 1, 0.3)

    result = np.zeros((len(noise_levels), ))
    for i, noise_level in enumerate(noise_levels):
        BER = sum(compute_BER("gardner", loop_gain, noise_level, 0.6) for _ in range(TEST_ITERATIONS))/TEST_ITERATIONS
        result[i] = BER
        print(f'N: {noise_level}, Gain: {loop_gain}, BER: {BER}')

    np.save("ber_Gardner_noise.npy", result)

    data = np.load("ber_Gardner_noise.npy")

    plt.plot(noise_levels, data)
    plt.xlabel('noise level')
    plt.title("BER for Gardner as a function noise level for a loop gain of 0.3 and symbol delay of 0.6")
    plt.ylabel('bit-error rate (BER)')
    plt.show()

