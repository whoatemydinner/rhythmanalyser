import matplotlib.pyplot as plt
from numpy import arange, sum as array_sum, histogram as nphist, mean
from scipy.signal import butter, sosfilt


class SoundEnergyBPMDetector:
    def __init__(self):
        self.block_length = 1024
        self.window_length = 43

        self.min_quaver_length = int(44100)

        self.windows = {}

        self.beat_map = [[], []]

        pass

    def estimate_tempo(self, signal, sr):
        if sr != 44100:
            self.min_quaver_length = int(sr)

        block_energies = []
        offset = 0

        beats = []

        # pass signal through LP filter
        # lp_filter = butter(1, 500, 'low', analog=False, fs=sr, output='sos')
        # signal = sosfilt(lp_filter, signal)

        while offset < len(signal):
            block_energies.append(self.get_block_energy(signal, offset))
            offset += self.block_length

        for i in range(0, len(block_energies)):
            window_energy, variance = self.get_average_window_energy_and_variance_for_block(block_energies, i)
            coefficient = -0.0000015 * variance + 1.5142857
            limit = coefficient * window_energy

            if block_energies[i][1] > limit:
                beats.append((block_energies[i][0], block_energies[i][1]))

        samples = []
        peaks = []
        for beat in beats:
            samples.append(beat[0])
            peaks.append(beat[1])

        max_peak = 0.0
        for peak in peaks:
            if peak > max_peak:
                max_peak = peak

        for i in range(0, len(peaks)):
            peaks[i] = peaks[i] / max_peak

        peak_clump_indice, peak_clump_values = self.get_peak_clumps(samples, peaks)

        histogram = self.get_tempo_histogram(peak_clump_indice, sr)



        probabilities = self.get_probabilities(histogram)
        self.create_beat_map(signal, sr, probabilities, peak_clump_indice)

        return probabilities

        # plt.figure()
        # plt.plot(signal)
        # # plt.plot(samples, peaks, 'ro')
        # plt.plot(peak_clump_indice, peak_clump_values, 'go')
        # plt.show()

    def get_block_energy(self, signal, offset):
        start_index = offset
        end_index = offset + self.block_length

        block_energy = 0.0

        for index in range(start_index, end_index):
            if index >= len(signal):
                break
            sample_energy = abs(signal[index])**2
            block_energy += sample_energy

        return offset, block_energy

    def get_average_window_energy_and_variance_for_block(self, block_energies, index):
        if index < self.window_length:
            window = self.get_window(block_energies, 0)
        else:
            window = self.get_window(block_energies, index - self.window_length)

        window_energy = 0.0

        for block_energy in window:
            sample_index = block_energy[0]
            instant_energy = block_energy[1]
            window_energy += instant_energy

        average_energy = window_energy / self.window_length

        subvariance = 0.0

        for block_energy in window:
            instant_energy = block_energy[1]
            subvariance += (average_energy - instant_energy)**2

        variance = subvariance / self.window_length

        return average_energy, variance

    def get_window(self, block_energies, index):
        if index not in self.windows.keys():
            self.windows[index] = block_energies[index:(index + self.window_length)]
        return self.windows[index]

    def get_peak_clumps(self, samples, peaks):
        minimum_distance = int(44100 * 60 / 180 / 2)

        print("minimum distance: " + str(minimum_distance))

        clusters = []

        for i in range(0, len(samples)):
            found_cluster = False
            for cluster in clusters:
                for element in cluster:
                    if samples[i] - element[0] == self.block_length:
                        cluster.append([samples[i], peaks[i]])
                        found_cluster = True
                        break
                if found_cluster:
                    break
            if not found_cluster:
                new_cluster = [[samples[i], peaks[i]]]
                clusters.append(new_cluster)

        clump_indice = []
        clump_value = []

        prev_clump = None
        for cluster in clusters:
            if prev_clump is not None:
                current_clump = cluster[0][0]
                if current_clump - prev_clump < minimum_distance:
                    continue
                else:
                    index = int(mean(self.get_indice_in_cluster(cluster)))
                    clump_indice.append(index)
                    clump_value.append(cluster[0][1])
                    prev_clump = current_clump
            else:
                index = int(mean(self.get_indice_in_cluster(cluster)))
                clump_indice.append(index)
                clump_value.append(cluster[0][1])
                prev_clump = cluster[0][0]

        return clump_indice, clump_value

    def get_tempo_histogram(self, peaks, sr):
        bpms = []

        prev_peak = None
        for peak in peaks:
            if prev_peak is not None:
                samples = peak - prev_peak
                tempo = sr / samples * 60
                while tempo >= 180.5:
                    tempo = tempo / 2.
                while tempo < 59.5:
                    tempo = tempo * 2.
                bpms.append(tempo)
            prev_peak = peak

        histogram = nphist(bpms, bins=arange(59.5, 180.5))

        # for index in range(0, len(histogram[0])):
        #     print("Entries for BPM " + str(histogram[1][index]) + ": " + str(histogram[0][index]))

        # plt.show()

        return histogram

    def get_probabilities(self, histogram):
        probabilites = []
        count = array_sum(histogram[0])

        for i in range(0, len(histogram[0])):
            times = histogram[0][i]
            tempo = histogram[1][i] + 0.5
            if times != 0.0:
                probabilites.append([tempo, times/count])

        return probabilites

    def create_beat_map(self, signal, sr, tempo_probabilities, beats):
        beat_map = []

        tempos = sorted(tempo_probabilities, key=lambda tup: tup[1], reverse=True)
        best_tempo = tempos[0][0]

        beat_length = 60. / best_tempo * sr

        print("BEAT LENGTH = " + str(beat_length))

        # bierzemy wywołanie i sprawdzamy w pięciu kolejnych znalezionych wywołaniach to najbliższe
        # zasugerowanemu przez tempo

        index = 0
        current_beat = beats[0]
        beat_map.append(current_beat)

        while index != len(beats) - 1:
            next_entries = get_n_next_entries_of_list_with_indexes(beats, index, 5)
            closest = get_closest_member(next_entries, current_beat + beat_length)

            index = closest[0]
            current_beat = closest[1]

            beat_map.append(current_beat)

        self.beat_map = beat_map

    def get_beat_map(self):
        return self.beat_map

    def get_indice_in_cluster(self, cluster):
        indice = []
        for peak in cluster:
            indice.append(peak[0])
        return indice


def get_n_next_entries_of_list_with_indexes(l, offset, n):
    if len(l) == offset + 1:
        return []
    elements = l[offset+1:offset+1+n] if len(l) > offset + n else l[offset+1:]

    entries = []

    for i in range(0, len(elements)):
        entries.append([offset + 1 + i, elements[i]])

    return entries


def get_closest_member(elements, value):
    elements_with_distance = []
    for element in elements:
        dist = abs(element[1] - value)
        elements_with_distance.append([dist, element[0], element[1]])

    print("\t", elements_with_distance)

    sorted_elements = sorted(elements_with_distance, key=lambda tup: tup[0])

    return [sorted_elements[0][1], sorted_elements[0][2]]
