import subprocess
import time
import threading
import util.logger as logger
import util.config as config

class AudioProcessor:
    def __init__(self):
        self.process = None
        self.thread = threading.Thread(target=self.process_audio, daemon=True)

    def start(self):
        self.thread.start()

    def process_audio(self):
        channels = config.value_of("audio_channels")
        rate = config.value_of("audio_sample_rate")
        format = config.value_of("audio_format")
        output_device = config.value_of("output_device")
        
        while True:
            self.process = subprocess.Popen(f'arecord -f {format} -r {rate} -c {channels} - | aplay -D {output_device} -', shell=True)
            while True:
                # コマンドの終了を確認
                if self.process.poll() is not None:
                    logger.error("Audio process has terminated, restarting...")
                    break
                time.sleep(1)

            # 標準出力とエラーを取得
            stdout, stderr = self.process.communicate()

            # 標準出力とエラーを表示
            logger.info("Audio process output:", stdout.decode())
            logger.error("Audio process error:", stderr.decode())

                
    def stop(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None
