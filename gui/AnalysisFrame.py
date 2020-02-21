from tkinter import IntVar, Radiobutton, Frame, Button
from enum import Enum
from tempo.LibrosaBPMDetector import LibrosaBPMDetector
from tempo.SoundEnergyBPMDetector import SoundEnergyBPMDetector
from tempo.DWTBPMDetector import DWTBPMDetector
from tempo.CombinedBPMDetector import CombinedBPMDetector
from audio.audiofile import get_audiofile, set_beatmap, draw_beatmap


class BPMDetector(Enum):
    librosa = 1
    dwt = 2
    se = 3
    combo = 4


class AnalysisFrame:
    def __init__(self, root):
        self.root = root

        self.frame = Frame(root.master)

        self.bpm_detection_id = IntVar(value=1)
        self.pack_bpm_detection_radio_buttons()

        self.analyse_button = Button(self.frame, text="Analyse audio", command=lambda: self.get_tempo())
        self.analyse_button.pack()

    def pack_bpm_detection_radio_buttons(self):
        Radiobutton(self.frame, text="Use librosa implementation", variable=self.bpm_detection_id,
                    value=BPMDetector.librosa.value).pack()
        Radiobutton(self.frame, text="Use DWT-based algorithm", variable=self.bpm_detection_id,
                    value=BPMDetector.dwt.value).pack()
        Radiobutton(self.frame, text="Use sound energy-based algorithm", variable=self.bpm_detection_id,
                    value=BPMDetector.se.value).pack()
        Radiobutton(self.frame, text="Use combined algorithms", variable=self.bpm_detection_id,
                    value=BPMDetector.combo.value).pack()

    def pack(self):
        self.frame.pack()

    def get_tempo(self):
        bpm_detector = self.choose_bpm_detector()

        if bpm_detector is None:
            print("Bah.")
            return
        else:
            audiofile, samplerate = get_audiofile()
            tempo = bpm_detector.estimate_tempo(audiofile, samplerate)
            print("Estimated tempo: " + str(tempo))

        if self.bpm_detection_id.get() == BPMDetector.se.value:
            set_beatmap(bpm_detector.beat_map)
            draw_beatmap()

    def choose_bpm_detector(self):
        id = self.bpm_detection_id.get()
        if id == BPMDetector.librosa.value:
            return LibrosaBPMDetector()
        elif id == BPMDetector.se.value:
            return SoundEnergyBPMDetector()
        elif id == BPMDetector.dwt.value:
            return DWTBPMDetector()
        elif id == BPMDetector.combo.value:
            return CombinedBPMDetector()
        else:
            return None