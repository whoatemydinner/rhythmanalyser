from tkinter import Tk, IntVar, Button
from gui import FileFrame, AnalysisFrame


class MainWindow:
    def __init__(self, filepath):
        self.master = Tk()
        self.master.wm_title("H")

        self.filepath = filepath

        self.preference = IntVar(value=1)

        self.file_frame = FileFrame.FileFrame(self, self.preference)
        self.file_frame.pack()

        self.analysis_frame = AnalysisFrame.AnalysisFrame(self)
        self.analysis_frame.pack()

    def accept_button_callback(self):
        print("Preference: " + str(self.preference.get()))

    def set_filepath(self, filepath):
        self.filepath = filepath

    def start(self):
        self.master.mainloop()
