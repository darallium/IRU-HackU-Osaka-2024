import os
import signal
import subprocess
import time
import threading
import util.logger as logger
import util.config as config

class AudioProcessor:
    def __init__(self):
        self.process = None
        self.is_stop = False
        self.thread = threading.Thread(target=self.process_audio, daemon=True)

    def start(self):
        self.is_stop = False
        self.thread.start()

    def process_audio(self):
        channels = config.value_of("audio_channels")
        rate = config.value_of("audio_sample_rate")
        format = config.value_of("audio_format")
        output_device = config.value_of("output_device")

        cmd = f"arecord -f {format} -r {str(rate)} -c {str(channels)} | aplay -"
        logger.info(f"Audio process command line: {cmd}")
        
        while not self.is_stop:
            self.process = subprocess.Popen(["bash", "-c", cmd], preexec_fn=os.setsid)
            while not self.is_stop:
                # コマンドの終了を確認
                if self.process.poll() is not None:
                    logger.error("Audio process has terminated, restarting...")
                    break

                time.sleep(1)
            if self.process is None:
                return

            # 標準出力とエラーを取得
            stdout, stderr = self.process.communicate()

            # 標準出力とエラーを表示
            if stdout:
                logger.info("Audio process output:", stdout.decode())
            if stderr:
                logger.error("Audio process error:", stderr.decode())

                
    def stop(self):
        if self.process is not None:
            self.is_stop = True
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
