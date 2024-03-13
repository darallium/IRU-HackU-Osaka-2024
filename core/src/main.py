# main.py
from image.azure_services import AzureServices
from image.processor import ImageProcessor
from util.font import download_font
import util.config as config
import util.logger as logger
import cv2
import time
import os

def main():

    download_font()

    azure_services = AzureServices(
        config.value_of('vision_key'),
        config.value_of('vision_endpoint'),
        config.value_of('translator_key'),
        config.value_of('translator_endpoint')
    )

    image_processor = ImageProcessor(azure_services)

    if os.name == 'nt':
        from audio.processor_win import AudioProcessor
    else:
        from audio.processor_linux import AudioProcessor

    audio_processor = AudioProcessor()
    cap = cv2.VideoCapture(config.value_of("camera_device_id"))
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    width = 1920
    height = 1080
    FPS = 60
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    if config.value_of("debug_mode"):
        cv2.namedWindow("HDMagIc")
    else:
        cv2.namedWindow("HDMagIc",cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("HDMagIc",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    audio_processor.start()

    while True:
        time_start = time.perf_counter()
        ret, frame = cap.read()
        if not ret:
            break

        frame = image_processor.process_frame(frame)
        
        if config.value_of("debug_mode"):
            # デバッグのために表示画面のサイズは半分にする
            height, width = frame.shape[:2]
            new_width = int(width * 0.5)
            new_height = int(height * 0.5)
            frame = cv2.resize(frame, (new_width, new_height))

        cv2.imshow("HDMagIc", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time_end = time.perf_counter()
        time.sleep(max(1.0 / FPS - (time_end- time_start) / 1000, 0.0))
        

    cap.release()
    cv2.destroyAllWindows()
    audio_processor.stop()

if __name__ == "__main__":
    main()
