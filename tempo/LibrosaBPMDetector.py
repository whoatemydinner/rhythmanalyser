from librosa.beat import tempo


class LibrosaBPMDetector:
    def __init__(self):
        pass

    def estimate_tempo(self, signal, sr):
        return [[int(tempo(signal, sr)), 1.0]]
