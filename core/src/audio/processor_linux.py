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
        
        while not self.is_stop:
            self.process = subprocess.Popen(f'arecord -f {format} -r {rate} -c {channels} - | aplay -', shell=True)
            while not self.is_stop:
                print(f"{self.is_stop}")
                try:
                    # コマンドの終了を確認
                    if self.process.poll() is not None:
                        logger.error("Audio process has terminated, restarting...")
                        print(f"{self.is_stop}")
                        break
                except:
                    print("Audio Error!!!")
                    return

                time.sleep(1)
            if self.process is None:
                return

            # 標準出力とエラーを取得
            stdout, stderr = self.process.communicate()
            print(f"{self.is_stop}")
            if self.is_stop:
                self.process.kill()

            # 標準出力とエラーを表示
            logger.info("Audio process output:", stdout.decode())
            logger.error("Audio process error:", stderr.decode())

                
    def stop(self):
        if self.process is not None:
            self.is_stop = True
            kill = subprocess.Popen(f"kill -9 {self.process.pid}", shell=True)
            self.process.kill()
            self.process.terminate()
            #self.process = None
