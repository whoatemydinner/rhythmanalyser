from tkinter import Frame, Radiobutton, Text, Button, filedialog, END, BOTTOM, BOTH, LEFT, messagebox, Label, BooleanVar
from librosa import display as libdisplay
import audio.audiofile as audiofile
import matplotlib.pyplot as plt
import matplotlib
from gui.AnalysisFrame import AnalysisFrame

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class FileFrame:
    def __init__(self, root, preference):
        # master facade (over Tkinter object)
        self.root = root
        # overall frame
        self.frame = Frame(root.master)

        label = Label(self.frame, text="File")
        label.pack(side=LEFT, fill=BOTH, expand=True)

        # preference object reference
        self.preference = preference

        # build and pack the file selection subframe
        self.text_field = self.pack_filepath_subframe(self.frame)

        # put in radio buttons
        pack_preference_radio_button(self.frame, self.preference)

        self.fig_canvas, self.figure, self.plot = self.pack_matplotlib_canvas()

        self.start_marker_position = 0.0
        self.end_marker_position = 0.0

        self.start_marker_edit = BooleanVar()

        Radiobutton(self.frame, text="Move start marker", variable=self.start_marker_edit,
                                    indicatoron=False, value=True).pack()
        Radiobutton(self.frame, text="Move end marker", variable=self.start_marker_edit,
                                    indicatoron=False, value=False).pack()

        self.trim_button = Button(self.frame, text="Trim audio to markers", command=lambda: self.trim_audio())
        self.trim_button.pack()

    def pack(self):
        self.frame.pack()

    def get_frame(self):
        return self.frame

    def pack_filepath_subframe(self, root):
        subframe = Frame(root)

        text = Text(subframe, state="disabled", height=1, width=60)
        text.pack()

        file_select_button = Button(subframe, text="Choose audio file...", command=lambda: self.get_filename())
        file_select_button.pack()

        file_load_button = Button(subframe, text="Load selected file", command=lambda: self.load_file())
        file_load_button.pack()

        subframe.pack()
        return text

    def update_text_field(self, string):
        self.text_field.configure(state="normal")
        self.text_field.delete(1.0, END)
        self.text_field.insert("1.0", string)
        self.text_field.configure(state="disabled")
        self.text_field.update()

    def get_filename(self):
        self.update_text_field(filedialog.askopenfilename(initialdir="~",
                                         title="Select audio file",
                                         filetypes=(("Wave files", "*.wav"),
                                                    ("MP3 files", "*.mp3"),
                                                    ("all files", "*.*"))))

    def load_file(self):
        filepath = self.text_field.get(1.0, END).rstrip()

        # reset
        self.start_marker_position = 0.0
        self.end_marker_position = 0.0

        if len(filepath) == 0 or filepath.isspace() or not filepath:
            messagebox.showerror("Error", "No file specified! Please select an audio file first.")

        signal, sr = audiofile.load(filepath, self.preference)
        print("File loaded!")

        # self.plot.clear()
        # libdisplay.waveplot(signal, sr, x_axis='time', ax=self.plot)
        # self.fig_canvas.draw()
        self.update_plot()
        print("Figure updated.")

        print(signal)
        print(audiofile.AUDIOFILE)

    def trim_audio(self):
        audiofile.trim_audiofile(self.start_marker_position, self.end_marker_position)
        self.start_marker_position = 0.0
        self.end_marker_position = 0.0
        self.update_plot()

    def on_plot_click(self, event):
        if self.start_marker_edit.get():
            if event.xdata > self.end_marker_position - 1:
                self.start_marker_position = self.end_marker_position - 1
            else:
                self.start_marker_position = event.xdata
        else:
            if event.xdata < self.start_marker_position + 1:
                self.end_marker_position = self.start_marker_position + 1
            else:
                self.end_marker_position = event.xdata
        self.update_plot()

    def update_plot(self):
        self.plot.clear()
        self.draw_audio_plot(audiofile.AUDIOFILE, audiofile.SAMPLERATE)
        self.draw_start_marker()
        self.draw_end_marker()
        self.fig_canvas.draw()

    def draw_audio_plot(self, signal, sr):
        libdisplay.waveplot(signal, sr, x_axis='time', ax=self.plot)

    def draw_start_marker(self):
        self.plot.axvline(x=self.start_marker_position, color='green')

    def draw_end_marker(self):
        self.plot.axvline(x=self.end_marker_position, color='red')

    def pack_matplotlib_canvas(self):
        f = Figure(figsize=(7, 2), dpi=100)
        ax = f.add_subplot(111)
        ax.get_yaxis().set_visible(False)
        f.patch.set_facecolor('#f0f0f0')
        canvas = FigureCanvasTkAgg(f, self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        canvas.mpl_connect('button_press_event', self.on_plot_click)

        return canvas, f, ax


def pack_preference_radio_button(frame, preference):
    Radiobutton(frame, text="Mixdown to mono", variable=preference, value=audiofile.ImportPreferences.mono.value).pack(side=LEFT)
    Radiobutton(frame, text="Use left channel", variable=preference, value=audiofile.ImportPreferences.left.value).pack(side=LEFT)
    Radiobutton(frame, text="Use right channel", variable=preference, value=audiofile.ImportPreferences.right.value).pack(side=LEFT)