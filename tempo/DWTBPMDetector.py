from numpy import arange, absolute, add, correlate, mean, ndarray, sum as array_sum, histogram as nphist
import matplotlib.pyplot as plt
import pywt


class LowPassFilter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.y = 0

    def reset(self):
        self.y = 0

    def filter(self, x):
        self.y = (1 - self.alpha) * x - self.alpha * self.y
        return self.y


class DWTBPMDetector:
    def __init__(self):
        # average expected sample rate is 44100 Hz
        self.window_size = int(44100 * 3)
        self.hop_size = self.window_size // 6
        self.bpms = []

    def estimate_tempo(self, signal, sr):
        # reset bpms
        self.bpms = []

        # adjust window size
        if sr != 44100:
            self.window_size = int(sr * 3)
            self.hop_size = self.window_size // 6

        offset = 0

        while offset + self.window_size < len(signal):
            end = offset + self.window_size if offset + self.window_size < len(signal) else len(signal)
            window = signal[offset:end]

            if len(window) < self.window_size:
                break

            self.bpms.extend(get_bpm_for_window(window, sr))

            offset += self.hop_size

        histogram = nphist(self.bpms, bins=arange(59.5, 180.5))

        # for index in range(0, len(histogram[0])):
        #     print("Entries for BPM " + str(histogram[1][index]) + ": " + str(histogram[0][index]))

        # plt.show()

        return get_probabilities(histogram)



def downsample(signal, factor):
    downsampled = []

    indice = arange(start=0, stop=len(signal), step=factor)

    for index in indice:
        downsampled.append(signal[index])

    return downsampled


def find_local_maximums(input: ndarray, top=None):
    maximums = []
    offset = 0
    window_size = 200

    # get max value from each set of [window_size] points
    while offset + window_size < len(input):
        end = offset + window_size if offset + window_size < len(input) else len(input)
        curr_max = [offset, input[offset]]
        for index in range(offset, end):
            if input[index] > curr_max[1]:
                curr_max = [index, input[index]]

        maximums.append(curr_max)
        offset += window_size

    if top is None:
        return maximums
    else:
        if isinstance(top, int):
            maximums = sorted(maximums, key=lambda tup: tup[1], reverse=True)
            return maximums[0:top]
        else:
            raise Exception("Argument top must be an integer")


def get_bpm_for_window(window, sample_rate):
    levels = 4
    approx_coeff = window
    detail_coeff_sum = None

    decimation = 2 ** (levels - 1)

    for level in range(0, levels):
        downsample_factor = 2 ** (levels - level - 1)
        detail_coeff, approx_coeff = pywt.dwt(approx_coeff, 'db4', 'reflect')

        detail_coeff = absolute(detail_coeff)
        detail_coeff = downsample(detail_coeff, downsample_factor)
        detail_coeff = detail_coeff - mean(detail_coeff)

        if detail_coeff_sum is None:
            detail_coeff_sum = detail_coeff
        else:
            if len(detail_coeff) < len(detail_coeff_sum):
                detail_coeff_sum = detail_coeff_sum[0:len(detail_coeff)]
            elif len(detail_coeff_sum) < len(detail_coeff):
                detail_coeff = detail_coeff[0:len(detail_coeff_sum)]

            detail_coeff_sum = add(detail_coeff_sum, detail_coeff)

    correlated = correlate(detail_coeff_sum, detail_coeff_sum, mode='full')
    correlated = correlated[correlated.size // 2:]

    maximums = find_local_maximums(correlated, 5)

    bpms = []

    for maximum in maximums:
        if maximum[0] == 0:
            continue

        location = maximum[0] * decimation
        period = location / sample_rate
        bpms.append(1 / period * 60.)

    return bpms


def get_probabilities(histogram):
    probabilites = []
    count = array_sum(histogram[0])

    for i in range(0, len(histogram[0])):
        times = histogram[0][i]
        tempo = histogram[1][i] + 0.5
        if times != 0.0:
            probabilites.append([tempo, times / count])

    return probabilites