from faster_whisper import WhisperModel
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile

model = WhisperModel("base", device="cpu", compute_type="int8")

def listen(duration = 5):
    sample_rate = 16000

    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")

    sd.wait()

    write("audio.wav", sample_rate, audio)

    segments ,info = model.transcribe("audio.wav")

    text = "".join(segment.text for segment in segments).strip()

    return text


def transcribe(audio_file):

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_file.read())

        segments, info = model.transcribe(f.name)

    text = "".join(segment.text for segment in segments).strip()

    return text