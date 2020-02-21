from tempo.LibrosaBPMDetector import LibrosaBPMDetector
from tempo.SoundEnergyBPMDetector import SoundEnergyBPMDetector
from tempo.DWTBPMDetector import DWTBPMDetector

class CombinedBPMDetector:
    def __init__(self):
        pass

    def estimate_tempo(self, signal, sr):
        # librosa -> waga 0.4
        # dwt -> waga 0.3
        # se -> waga 0.3

        probability_bucket = {}

        print(" = = LIBROSA = = ")
        lib = LibrosaBPMDetector().estimate_tempo(signal, sr)
        probability_bucket[lib[0][0]] = lib[0][1] * 0.4
        print(" = = SOUND ENERGY = = ")
        se = SoundEnergyBPMDetector().estimate_tempo(signal, sr)
        print(" = = DWT = = ")
        print(DWTBPMDetector().estimate_tempo(signal, sr))