import librosa
from application.util import SingletonMeta

AUDIO = None
SAMPLE_RATE = None

TRIMMED_AUDIO = None


class AudioData(metaclass=SingletonMeta):
    data = None
    sample_rate = None

    def __init__(self):
        pass

    def load_audio(self, filepath, sr=None, mono=True):
        self.data, self.sample_rate = librosa.load(filepath, sr, mono, offset=0.0)

    def replace_audio(self, replacing):
        self.data = replacing


def load(filepath):
    global AUDIO, SAMPLE_RATE
    exception = None

    # always keep the native, original sampling rate
    sr = None
    mono = True

    AUDIO, SAMPLE_RATE = librosa.load(filepath, sr, mono, offset=0.0)


def get_audio():
    global AUDIO, SAMPLE_RATE

    if AUDIO is not None and SAMPLE_RATE is not None:
        return AUDIO, SAMPLE_RATE
    else:
        raise Exception


def trim_audio(ts, te):
    global SAMPLE_RATE, TRIMMED_AUDIO
    start_sample = int(ts * SAMPLE_RATE)
    end_sample = int(te * SAMPLE_RATE)

    TRIMMED_AUDIO = TRIMMED_AUDIO[start_sample:end_sample]


def replace_audio():
    global AUDIO, TRIMMED_AUDIO

    if TRIMMED_AUDIO is not None:
        AUDIO = TRIMMED_AUDIO
        TRIMMED_AUDIO = None
