import pyaudio
import threading
import util.logger as logger
import util.config as config

class AudioProcessor:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None

    def start(self):
        channels = config.value_of("audio_channels")
        rate = config.value_of("audio_sample_rate")

        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,
            input=True,
            output=True,
            input_device_index=config.value_of("input_device_index"),
            output_device_index=config.value_of("output_device_index"),
            frames_per_buffer=config.value_of("audio_buffer_size"))

        self.thread = threading.Thread(target=self.process_audio, daemon=True)
        self.thread.start()

    def process_audio(self):
        while self.stream.is_active():
            data = self.stream.read(config.value_of("audio_buffer_size"))
            self.stream.write(data)

    def stop(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
