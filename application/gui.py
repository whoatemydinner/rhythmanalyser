import tkinter as tk
from tkinter import filedialog


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

        self.text_field = self.pack_filepath_subframe()

        label = tk.Label(self.frame, text="File")
        label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def pack(self):
        self.frame.pack()

    def pack_filepath_subframe(self):
        subframe = tk.Frame(self.frame)

        text = tk.Text(subframe, state="disabled", height=1, width=60)
        text.pack()

        file_select_button = tk.Button(subframe, text="Choose audio file...", command=lambda: self.get_filename())
        file_select_button.pack()

        file_load_button = tk.Button(subframe, text="Load selected file", command=lambda: self.load_file())
        file_load_button.pack()

        subframe.pack()
        return text

    def get_filename(self):
        self.update_text_field(tk.filedialog.askopenfilename(initialdir="~",
                                                             title="Select audio file",
                                                             filetypes=(("Wave files", "*.wav"),
                                                                        ("MP3 files", "*.mp3"),
                                                                        ("all files", "*.*"))))

    def update_text_field(self, string):
        self.text_field.configure(state="normal")
        self.text_field.delete(1.0, tk.END)
        self.text_field.insert("1.0", string)
        self.text_field.configure(state="disabled")
        self.text_field.update()


class AnalysisFrame:
    def __init__(self, root):
        # master facade (over Tkinter object)
        self.root = root
        # overall frame
        self.frame = tk.Frame(root.master)

    def pack(self):
        self.frame.pack()
