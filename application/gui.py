import tkinter as tk
from tkinter import BooleanVar
from application import audio
from tkinter import filedialog, messagebox
import numpy as np
import math
from librosa import display as libdisplay

# matplotlib
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
matplotlib.use("TkAgg")


trim_window = None


def get_trim_window(launching_root):
    global trim_window

    if trim_window is None:
        trim_window = TrimWindow(launching_root)
    else:
        pass


class MainWindow:
    def __init__(self):
        self.master = tk.Tk()
        self.master.wm_title("Rhythm Analyser")

        self.file_frame = FileFrame(self)
        self.file_frame.pack()

    def start(self):
        self.master.mainloop()


# Frame which organizes the section of the window connected to opening and trimming the audio file
class FileFrame:
    def __init__(self, root):
        # master facade (over Tkinter object)
        self.root = root
        # overall frame
        self.frame = tk.Frame(root.master)

        self.start_marker_position = 0.0
        self.end_marker_position = 0.0

        self.filepath_field, self.load_file_button, self.edit_button, self.audio_file_canvas \
            = self.pack_filepath_subframe()

    def pack(self):
        self.frame.pack()

    def pack_filepath_subframe(self):
        subframe = tk.Frame(self.frame)
        subframe.grid()

        label = tk.Label(subframe, text="File")
        label.grid(row=0, sticky=tk.W, padx=5, pady=5)

        text = tk.Text(subframe, state="disabled", height=1, width=60)
        text.grid(row=1, columnspan=3, padx=5, pady=5)

        button_subframe = tk.Frame(subframe)
        button_subframe.grid(row=2, column=2)

        file_load_button = tk.Button(button_subframe, text="Load", command=lambda: self.load_file())
        file_load_button.pack(side=tk.RIGHT, padx=5, pady=5)

        edit_button = tk.Button(button_subframe, text="Trim", command=lambda: get_trim_window(self.frame))
        edit_button.pack(side=tk.RIGHT, padx=5, pady=5)
        edit_button['state'] = 'disabled'

        audio_file_canvas = tk.Canvas(subframe, width=500, height=100)
        audio_file_canvas.grid(row=3, columnspan=3, padx=5, pady=5)

        return text, file_load_button, edit_button, audio_file_canvas

    def get_filename(self):
        self.update_text_field(tk.filedialog.askopenfilename(initialdir="~",
                                                             title="Select audio file",
                                                             filetypes=(("audio files", "*.wav *.mp3 *.ogg *.flac"),
                                                                        ("all files", "*.*"))))

    def update_text_field(self, string):
        self.filepath_field.configure(state="normal")
        self.filepath_field.delete(1.0, tk.END)
        self.filepath_field.insert("1.0", string)
        self.filepath_field.configure(state="disabled")
        self.filepath_field.update()

    def load_file(self):
        self.edit_button['state'] = 'disabled'

        self.get_filename()

        filepath = self.filepath_field.get(1.0, tk.END).rstrip()

        # reset
        self.start_marker_position = 0.0
        self.end_marker_position = 0.0

        if len(filepath) == 0 or filepath.isspace() or not filepath:
            messagebox.showerror("Error", "No file specified! Please select an audio file first.")

        audio.load(filepath)

        audio_file, sample_rate = audio.get_audio()

        # 500 points
        dist_between_points = len(audio_file) / 500.

        waveform_points = []
        offset = 0

        while offset < len(audio_file) or len(waveform_points) <= 500:
            if offset < len(audio_file):
                waveform_points.append(audio_file[offset])
            else:
                waveform_points.append(0.)
            offset += int(dist_between_points)

        if len(waveform_points) > 500:
            waveform_points = waveform_points[0:500]

        waveform_points = np.add(np.multiply(waveform_points, 50.), 50.)
        waveform_x_axis = range(0, 500)

        waveform = []

        for i in range(0, 1000):
            index = int(math.floor(i / 2.))
            if i % 2 == 0:
                waveform.append(waveform_x_axis[index])
            else:
                waveform.append(waveform_points[index])

        self.audio_file_canvas.create_line(smooth=1, *waveform)
        self.audio_file_canvas.update()

        self.edit_button['state'] = 'normal'

        print("File loaded!")


class AnalysisFrame:
    def __init__(self, root):
        # master facade (over Tkinter object)
        self.root = root
        # overall frame
        self.frame = tk.Frame(root.master)

    def pack(self):
        self.frame.pack()


class TrimWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)

        audio.TRIMMED_AUDIO = audio.get_audio()[0]
        self.start_marker_position = 0.0
        self.end_marker_position = (len(audio.TRIMMED_AUDIO) + 1.) / audio.SAMPLE_RATE
        self.start_marker_edit = BooleanVar()
        self.start_marker_edit.set('false')
        self.end_marker_edit = BooleanVar()
        self.end_marker_edit.set('false')

        self.frame = tk.Frame(self.window)
        self.frame.grid()
        self.start_marker_button = \
            tk.Button(self.frame, text="Move start marker", relief="raised", command=self.toggle_start_marker_button)
        self.start_marker_button.grid(row=0, column=0, padx=5, pady=5)
        self.end_marker_button = \
            tk.Button(self.frame, text="Move end marker", relief="raised", command=self.toggle_end_marker_button)
        self.end_marker_button.grid(row=0, column=1, padx=5, pady=5)

        self.plot_canvas, self.plot_figure, self.plot_axes = self.get_matplotlib_canvas()
        self.plot_canvas.get_tk_widget().grid(row=1, columnspan=2, column=0, padx=5, pady=5)

        self.trim_button = \
            tk.Button(self.frame, text="Trim to markers", command=self.trim_audio)
        self.trim_button.grid(row=2, column=0, padx=5, pady=5)
        self.accept_button = tk.Button(self.frame, text="OK", command=self.replace_audio)
        self.accept_button.grid(row=2, column=1, padx=5, pady=5)

        self.update_plot()

        self.window.update()

        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", self.kill_trim_window)

    def get_matplotlib_canvas(self):
        f = Figure(figsize=(7, 2), dpi=100)
        ax = f.add_subplot(111)
        ax.get_yaxis().set_visible(False)
        f.patch.set_facecolor(self.frame["background"])
        canvas = FigureCanvasTkAgg(f, self.frame)
        canvas.draw()
        canvas.mpl_connect('button_press_event', self.on_plot_click)
        return canvas, f, ax

    def update_plot(self):
        self.plot_axes.clear()
        self.draw_audio_plot(audio.TRIMMED_AUDIO, audio.SAMPLE_RATE)
        self.draw_start_marker()
        self.draw_end_marker()
        self.plot_canvas.draw()

    def on_plot_click(self, event):
        print('start:' + str(self.start_marker_edit.get()))
        print('end:' + str(self.end_marker_edit.get()))
        if self.start_marker_edit.get():
            if event.xdata > self.end_marker_position - 0.01:
                self.start_marker_position = self.end_marker_position - 1
            else:
                self.start_marker_position = event.xdata
        if self.end_marker_edit.get():
            if event.xdata < self.start_marker_position + 0.01:
                self.end_marker_position = self.start_marker_position + 1
            else:
                self.end_marker_position = event.xdata
        self.update_plot()

    def draw_start_marker(self):
        self.plot_axes.axvline(x=self.start_marker_position, color='green')

    def draw_end_marker(self):
        self.plot_axes.axvline(x=self.end_marker_position, color='red')

    def draw_audio_plot(self, signal, sr):
        libdisplay.waveplot(signal, sr, x_axis='time', ax=self.plot_axes)

    def toggle_start_marker_button(self):
        if self.start_marker_button.config('relief')[-1] == 'sunken':
            self.start_marker_button.config(relief="raised")
            self.start_marker_edit.set('false')
        else:
            if self.end_marker_button.config('relief')[-1] == 'sunken':
                self.end_marker_button.config(relief="raised")
                self.end_marker_edit.set('false')
            self.start_marker_button.config(relief="sunken")
            self.start_marker_edit.set('true')

    def toggle_end_marker_button(self):
        if self.end_marker_button.config('relief')[-1] == 'sunken':
            self.end_marker_button.config(relief="raised")
            self.end_marker_edit.set('false')
        else:
            if self.start_marker_button.config('relief')[-1] == 'sunken':
                self.start_marker_button.config(relief="raised")
                self.start_marker_edit.set('false')
            self.end_marker_button.config(relief="sunken")
            self.end_marker_edit.set('true')

    def trim_audio(self):
        audio.trim_audio(self.start_marker_position, self.end_marker_position)
        self.start_marker_position = 0.0
        self.end_marker_position = (len(audio.TRIMMED_AUDIO) + 1.) / audio.SAMPLE_RATE
        self.update_plot()

    def replace_audio(self):
        audio.replace_audio()

    def kill_trim_window(self):
        global trim_window

        trim_window = None
        self.window.destroy()
