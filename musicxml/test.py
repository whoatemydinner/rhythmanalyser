from musicxml import instruments, measure
import matplotlib.pyplot as plt
from scipy import fft, signal as spsignal
from librosa.core import load as libload
from librosa.effects import percussive
from librosa.output import write_wav
from numpy import amax, mean, arange, linspace, log10, logspace, log, multiply, add, power, sum, divide, correlate
import sys


# meter = [4, 4]
# snare_index = 0
# kick_index = 1
#
# measure_beats = [
#     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
# ]
#
# # measure = measure.Measure(tempo=120, number=1, meter=meter)
# #
# # measure.beats_to_notes(measure_beats)
# # measure.print_measure()
#
# h = [
#     [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#     [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
# ]
#
# g = [
#     [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
#     [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1]
# ]


# def flatten_beats(beats):
#     flattened = []
#
#     if len(beats) != 2:
#         raise Exception
#
#     if len(beats[snare_index]) != len(beats[kick_index]):
#         raise Exception
#
#     for index in range(0, len(beats[snare_index])):
#         kick = beats[kick_index][index]
#         snare = beats[snare_index][index]
#
#         if kick == 1 and snare == 1:
#             flattened.append("BS")
#         elif kick == 1 and snare == 0:
#             flattened.append("B")
#         elif kick == 0 and snare == 1:
#             flattened.append("S")
#         else:
#             flattened.append("-")
#
#     return flattened
#
#
# def get_window(array, length):
#     return array[0:length]
#
#
# def compare_with_following(array, window):
#     if len(array) < len(window)*2:
#         raise Exception
#
#     following = array[len(window):len(window)*2]
#
#     #print(window)
#     #print('vs.')
#     #print(following)
#
#     similarity_array = []
#
#     for index in range(0, len(window)):
#         similarity_array.append(similarity_of_beat(window[index], following[index]))
#
#     #print(similarity_array)
#
#     max_similarity = len(similarity_array)*1.0
#     similarity_sum = 0.0
#     for entry in similarity_array:
#         similarity_sum += entry
#
#     similarity_coefficient = similarity_sum / max_similarity
#
#     return similarity_coefficient
#
#
# def similarity_of_beat(i, j):
#     if i == j:
#         return 0.9
#     if i == 'B' and j == 'S':
#         return 0.1
#     if i == 'S' and j == 'B':
#         return 0.1
#     if i == 'S' and j == 'BS':
#         return 0.6
#     if i == 'BS' and j == 'S':
#         return 0.6
#     if i == 'B' and j == 'BS':
#         return 0.2
#     else:
#         return 0.2
#

# flat_h = flatten_beats(h)
# flat_g = flatten_beats(g)
#
# for i in range(3, 8):
#     similarity = compare_with_following(flat_h, get_window(flat_g, i))
#     print('Similarity coefficient for window length ' + str(i) + ' is ' + str(similarity))

# def get_n_next_entries_of_list_with_indexes(l, offset, n):
#     if len(l) == offset + 1:
#         return []
#     elements = l[offset+1:offset+1+n] if len(l) > offset + n else l[offset+1:]
#
#     entries = []
#
#     for i in range(0, len(elements)):
#         entries.append([offset + 1 + i, elements[i]])
#
#     return entries
#
# def get_closest_member(elements, value):
#     elements_with_distance = []
#     for element in elements:
#         dist = abs(element[1] - value)
#         elements_with_distance.append([dist, element[0], element[1]])
#
#     sorted_elements = sorted(elements_with_distance, key=lambda tup: tup[0])
#
#     return [sorted_elements[0][1], sorted_elements[0][2]]
#
#
# seq = [1000, 2000, 3000, 3790, 3990, 5000, 6000, 7000, 7040, 7990, 8000, 9000, 10000]
# index = 0
# val = seq[index]
# period = 1000
#
# print(index, val)
#
# while index != len(seq) - 1:
#     next_entries = get_n_next_entries_of_list_with_indexes(seq, index, 5)
#     closest = get_closest_member(next_entries, val + period)
#
#     index = closest[0]
#     val = closest[1]
#
#     print(index, val)

# file = '/home/kierzek/rhythms/fmo.wav'
# signal, sample_rate = libload(file, None, True, offset=0.0)
#
# f, t, Sxx = spsignal.spectrogram(signal, sample_rate, spsignal.get_window('hamming', 1024), noverlap=512,
#                                  mode='magnitude')

# for index in range(0, len(Sxx[0])):
#     print(f[index], Sxx[0][index])

# f = f[0:177]
# Sxx = Sxx[0:177]
# samples = t * sample_rate
#
# plt.pcolormesh(samples, f, Sxx)
# plt.show()

#
# X = fft.fft(signal)
# freqs = fft.fftfreq(len(signal)) * sample_rate

#
# plt.plot(freqs, npabs(X))
# plt.show()

# cost = [[1, 2, 3],
#         [4, 8, 2],
#         [1, 5, 3]]
#
# print(diagonal(cost, -1))

#
#
# def find_min_cost(matrix, i, j):
#     if i < 0 or j < 0:
#         return sys.maxsize
#     elif i == 0 and j == 0:
#         return matrix[i][j]
#     else:
#         minimum = min(find_min_cost(matrix, i - 1, j - 1),
#                       find_min_cost(matrix, i - 1, j),
#                       find_min_cost(matrix, i, j - 1))
#         print(minimum)
#         return matrix[i][j] + minimum
#
#
# print(find_min_cost(cost, 2, 2))

# window = 1024 (23 ms)
# overlap = 512 (50%)


def window_signal(win, sig):
    windowed = []

    offset = 0
    hop = 512

    while offset + len(win) <= len(sig):
        winsig = multiply(sig[offset:offset + len(win)], win)
        windowed.append(winsig)
        offset += hop
    return windowed


def calculate_power_in_window(window):
    return sum(power(window, 2)) / len(window)


def get_signal_in_bands(signal, filter_bank):
    signal_in_bands = []
    for filt in filter_bank:
        signal_in_bands.append(spsignal.sosfilt(filt, signal))
    return signal_in_bands


def perform_u_law_algorithm(data, u):
    return divide(log(1 + multiply(u, data)), log(1 + u))


def differentiante(data):
    differentiated = []
    for sample_index in range(0, len(data)):
        prev_sample = data[sample_index - 1] if sample_index > 0 else 0.
        curr_sample = data[sample_index]

        difference = curr_sample - prev_sample

        differentiated.append(difference if difference > 0 else 0)
    return differentiated


def interpolate(data, factor):
    interpolated = []
    if factor <= 0:
        raise Exception
    for sample_index in range(0, len(data)):
        if sample_index != len(data) - 1:
            interpolated.append(data[sample_index])
            for sub_index in range(0, factor - 1):
                interpolated.append(0.)
        else:
            interpolated.append(data[sample_index])
    return interpolated


def create_critical_band_filters():
    # critical bands according to Bark scale
    filters = []
    filters.append(spsignal.butter(6, [20, 100], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [100, 200], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [200, 300], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [300, 400], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [400, 510], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [510, 630], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [630, 770], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [770, 920], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [920, 1080], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [1080, 1270], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [1270, 1480], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [1480, 1720], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [1720, 2000], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [2000, 2320], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [2320, 2700], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [2700, 3150], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [3150, 3700], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [3700, 4400], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [4400, 5300], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [5300, 6400], btype='bandpass', analog=False, output='sos', fs=44100))
    filters.append(spsignal.butter(6, [6400, 7700], btype='bandpass', analog=False, output='sos', fs=44100))
    return filters


fil_bank = create_critical_band_filters()

window = spsignal.get_window('hann', 1024)

data, sample_rate = libload("/home/kierzek/rhythms/4 80.wav", mono=True, sr=44100)
data = percussive(data)
# data, sample_rate = libload("/media/kierzek/Moar/muzyczka/complete/MGMT/MGMT - Little Dark Age.mp3", mono=True, sr=44100)
data_mean = mean(data)
# plt.plot(arange(0, len(data)), data)
for index in range(0, len(data)):
    data[index] = data[index] - data_mean

bandpassed = get_signal_in_bands(data, fil_bank)

bands = []

for band_index in range(0, len(bandpassed)):
    print("Processing band " + str(band_index) + "...")
    band = bandpassed[band_index]
    power_in_windows = []
    windows = window_signal(spsignal.get_window("hann", 1024), band)
    for window in windows:
        power_in_windows.append(calculate_power_in_window(window))
    bands.append(power_in_windows)

smoothing_filter = spsignal.butter(2, 10, btype='lowpass', analog=False, output='sos', fs=172)

for band_index in range(0, len(bands)):
    bands[band_index] = spsignal.sosfilt(smoothing_filter,
                                         interpolate(perform_u_law_algorithm(bands[band_index], 100), 2))

differentiated_bands = []
for band_index in range(0, len(bands)):
    bands[band_index] = perform_u_law_algorithm(bands[band_index], 100)
    differentiated_bands.append(differentiante(bands[band_index]))

# weighted average
lam = 0.8

weighted_bands = []
for band_index in range(0, len(bands)):
    band = bands[band_index]
    diff_band = differentiated_bands[band_index]

    weighted_band = multiply((1 - lam), band) + multiply(lam * 172. / 10., diff_band)
    for sample_index in range(0, len(weighted_band)):
        if weighted_band[sample_index] < 0:
            weighted_band[sample_index] = 0.

    weighted_bands.append(weighted_band)


#
# autocorrelation = correlate(weighted_channels, weighted_channels, mode='full')
# autocorrelation = autocorrelation[autocorrelation.size//2:]

# peaks = spsignal.find_peaks(autocorrelation, amax(autocorrelation) * 0.5, 2)
# for peak in peaks[0]:
#     plt.axvline(peak)
#     print()

# comb filter periods
periods = range(50, 260)
equivalent_tempos = divide((60 * 44100), multiply(periods, 256))

for p_i in range(0, len(periods)):
    print(periods[p_i], equivalent_tempos[p_i])

# plt.plot(range(0, len(channels[0])), channels[0])
# plt.plot(range(0, len(channels[1])), channels[1])
# plt.plot(range(0, len(channels[2])), channels[2])
# plt.plot(range(0, len(weighted_channels)), weighted_channels)
# plt.plot(range(0, len(autocorrelation)), autocorrelation)
plt.show()

# print(sample_rate)
#
# perc = percussive(data)

# logged_signal = []
# # for fs in filtered_signal:
# band = []
# mi = 100.
# for sample in filtered_signal[0]:
#         band.append(log(1 + mi * sample) / log(1 + mi))
# logged_signal.append(band)
#
# # differential
# diff = []
# diff.append([])
#
# for index in range(0, len(logged_signal[0])):
#         differential = logged_signal[0][index] - logged_signal[0][index - 1] if index > 0 else logged_signal[0][index]
#         diff[0].append(differential)
#
# # HWR
# for index in range(0, len(diff[0])):
#         half_wave_rectified = diff[0][index] if diff[0][index] > 0 else 0
#         diff[0][index] = half_wave_rectified
#
# weighted = []
# weighted.append([])
#
# lam = 0.8
# for index in range(0, len(diff[0])):
#         avg = (1 - lam) * logged_signal[0][index] + lam * diff[0][index]
#         weighted[0].append(avg)
#
# plt.plot(arange(0, len(data)), weighted[0])
# plt.show()

# f, t, Sxx = spsignal.spectrogram(data, fs=sample_rate, window=spsignal.get_window("hann", 1024), noverlap=512, mode="magnitude")
# plt.pcolormesh(t, f, Sxx)
# plt.show()

# for freq in f:
#         print(freq)

# f, t, Sxx = spsignal.spectrogram(data, fs=sample_rate, window=spsignal.get_window("hann", 1024), noverlap=512, mode="magnitude")
# # plt.pcolormesh(t, f, Sxx)
# plt.plot(arange(0, len(data)), data)
# plt.show()
#
# write_wav("/home/kierzek/rhythms/ls_perc.wav", y=perc, sr=sample_rate)
