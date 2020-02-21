from librosa.core import load as libload
from enum import Enum
import matplotlib.pyplot as plt
from numpy import arange, zeros, dot, linalg, diagonal, mean
from scipy import signal as sig

# we are going to use these fields as a singleton
AUDIOFILE = None
AUDIOFILE_PERC = None
SAMPLERATE = 0
BEATMAP = []

class ImportPreferences(Enum):
    mono = 1
    left = 2
    right = 3


def load(filepath, import_pref):
    exception = None

    if import_pref is not None:
        if not isinstance(import_pref, int):
            import_pref = import_pref.get()

    # always keep the native, original sampling rate
    sr = None

    # mixdown to mono if requested, otherwise at the end left or right channel is selected
    # we work on mono signals as it can be assumed that left and right channels are corelated
    mono = import_pref == ImportPreferences.mono.value

    print("import pref: " + str(import_pref))

    signal, sample_rate = libload(filepath, sr, mono, offset=0.0)

    if signal.ndim > 1:
        if import_pref == 2:
            signal = signal[0]
        elif import_pref == 3:
            signal = signal[1]
        else:
            pass

    set_audiofile(signal, sample_rate)

    return signal, sample_rate


def trim_audiofile(ts, te):
    global SAMPLERATE, AUDIOFILE
    start_sample = int(ts * SAMPLERATE)
    end_sample = int(te * SAMPLERATE)

    set_audiofile(AUDIOFILE[start_sample:end_sample], SAMPLERATE)


def set_audiofile(audiofile, samplerate):
    global AUDIOFILE
    global SAMPLERATE

    AUDIOFILE = audiofile
    SAMPLERATE = samplerate


def get_audiofile():
    global AUDIOFILE
    global SAMPLERATE

    return AUDIOFILE, SAMPLERATE


def set_beatmap(beat_map):
    global BEATMAP

    BEATMAP = beat_map


def get_beatmap():
    global BEATMAP

    return BEATMAP

def draw_beatmap():
    global AUDIOFILE, BEATMAP, SAMPLERATE
    peak_energies = []
    for peak in BEATMAP:
        start = peak - 2000
        if start < 0:
            start = 0
        end = peak + 2001
        if end > len(AUDIOFILE):
            end = len(AUDIOFILE)

        f, t, Sxx = sig.spectrogram(AUDIOFILE[start:end], SAMPLERATE, sig.get_window('hamming', 1024), noverlap=512,
                                         mode='magnitude')

        f = f[0:177]
        Sxx = Sxx[0:177]
        samples = t * SAMPLERATE

        average_energy = []
        for freq_index in range(0, len(f)):
            summed_energy = 0
            for sample_index in range(0, len(samples)):
                energy = abs(Sxx[freq_index][sample_index])
                summed_energy += energy

            average_energy.append(summed_energy / len(samples))

        peak_energies.append([peak, average_energy])

    matrix = zeros((len(peak_energies), len(peak_energies)))

    for ref_peak_index in range(0, len(peak_energies)):
        for comp_peak_index in range(0, len(peak_energies)):
            matrix[ref_peak_index][comp_peak_index] = \
                get_cosine_of_two_peaks(peak_energies[ref_peak_index], ref_peak_index,
                                        peak_energies[comp_peak_index], comp_peak_index)



    # plt.plot(arange(0, len(AUDIOFILE)), AUDIOFILE)
    # for peak in BEATMAP:
    #     plt.axvline(x=peak, color='orange')
    # plt.show()

    # plt.matshow(matrix)
    # plt.show()

    min_offset = 0
    max_offset = len(matrix)

    diagonal_means = []
    offsets = arange(min_offset, max_offset)
    for offset in offsets:
        diagonal_offset = diagonal(matrix, offset)
        diagonal_means.append(mean(diagonal_offset))

    plt.plot(arange(1, len(diagonal_means) + 1), diagonal_means)
    plt.show()

    # diagonal = []
    # for index in range(0, len(matrix)):
    #     diagonal.append(matrix[index][index])

    # plt.plot(arange(0, len(matrix)), diagonal)
    # plt.show()

def get_cosine_of_two_peaks(ref_peak, ref_peak_index, comp_peak, comp_peak_index):
    # indice definitions
    peak_sample = 0
    bin_index = 1

    # product = 0.
    # ref_magnitude = 0.
    # comp_magnitude = 0.
    #
    # for f in range(0, len(ref_peak[bin_index])):
    #     ref_energy = ref_peak[bin_index][f]
    #     comp_energy = comp_peak[bin_index][f]
    #
    #     product += ref_energy * comp_energy
    #     ref_magnitude += abs(ref_energy)
    #     comp_magnitude += abs(comp_energy)

    product = dot(ref_peak[bin_index], comp_peak[bin_index])
    ref_magnitude = linalg.norm(ref_peak[bin_index])
    comp_magnitude = linalg.norm(comp_peak[bin_index])

    # if ref_peak_index == comp_peak_index:
    #     print(ref_peak_index, comp_peak_index, product / (ref_magnitude * comp_magnitude))

    return product / (ref_magnitude * comp_magnitude)
