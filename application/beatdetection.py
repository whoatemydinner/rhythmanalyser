import pywt
import numpy as np

ID_DWT = 1
ID_FULL_ENERGY = 2
ID_BAND_ENERGY = 3


class WaveletNoveltyFunctionGenerator:
    def __init__(self):
        # set number of decomposition steps at recommended 4
        self.decomposition_levels = 4

    def get_novelty_function(self, audio_signal):
        approx_coefficient = audio_signal
        detail_coefficient = None

        decimation = 2 ** (self.decomposition_levels - 1)

        for level in range(0, self.decomposition_levels):
            downsample_factor = 2 ** (self.decomposition_levels - level - 1)

            sub_detail_coefficient, approx_coefficient = pywt.dwt(approx_coefficient, 'db4', 'reflect')

            sub_detail_coefficient = np.absolute(sub_detail_coefficient)
            sub_detail_coefficient = downsample(sub_detail_coefficient, downsample_factor)
            sub_detail_coefficient = sub_detail_coefficient - np.mean(sub_detail_coefficient)

            if detail_coefficient is None:
                detail_coefficient = sub_detail_coefficient
            else:
                if len(sub_detail_coefficient) < len(detail_coefficient):
                    detail_coefficient = detail_coefficient[0:len(sub_detail_coefficient)]
                elif len(sub_detail_coefficient) > len(detail_coefficient):
                    sub_detail_coefficient = sub_detail_coefficient[0:len(detail_coefficient)]

                detail_coefficient = np.add(detail_coefficient, sub_detail_coefficient)

        return detail_coefficient


class FullEnergyNoveltyFunctionGenerator:
    def __init__(self):
        pass


class BandEnergyNoveltyFunctionGenerator:
    def __init__(self):
        pass


def get_novelty_function_generator(gen_id: int):
    if gen_id == ID_DWT:
        return WaveletNoveltyFunctionGenerator()
    elif gen_id == ID_FULL_ENERGY:
        return FullEnergyNoveltyFunctionGenerator()
    elif gen_id == ID_BAND_ENERGY:
        return BandEnergyNoveltyFunctionGenerator()

def downsample(data, factor):
    downsampled = []

    indice = np.arange(start=0, stop=len(data), step=factor)

    for index in indice:
        downsampled.append(data[index])

    return downsampled
