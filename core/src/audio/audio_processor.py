# audio_processor.py
import pyaudio

class AudioProcessor:
    def __init__(self):
        self.p = pyaudio.PyAudio()

    def start(self):
        stream = self.p.open(format=pyaudio.paInt16,
                             channels=1,
                             rate=44100,
                             input=True,
                             output=True,
                             frames_per_buffer=1024)
        while True:
            data = stream.read(1024)
            stream.write(data)

    def stop(self):
        stream.stop_stream()
        stream.close()
        self.p.terminate()