# main.py
from image.azure_services import AzureServices
from image.processor import ImageProcessor
from audio.processor import AudioProcessor

import util.config as config
import util.logger as logger
import cv2
import numpy as np
import time
import json
import asyncio

def main():

    azure_services = AzureServices(
        config.value_of('vision_key'),
        config.value_of('vision_endpoint'),
        config.value_of('translator_key'),
        config.value_of('translator_endpoint')
    )

    image_processor = ImageProcessor(azure_services)
    audio_processor = AudioProcessor()
    cap = cv2.VideoCapture(config.value_of("camera_device_id"))
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    width = 1920
    height = 1080
    FPS = 60
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    audio_processor.start()

    while True:
        time_start = time.perf_counter()
        ret, frame = cap.read()
        if not ret:
            break

        frame = image_processor.process_frame(frame)

        # デバッグのために表示画面のサイズは半分にする
        # 画像の高さと幅を取得
        height, width = frame.shape[:2]

        # 新しいサイズを指定（ここでは元のサイズの半分）
        new_width = int(width * 0.5)
        new_height = int(height * 0.5)

        # 画像のリサイズ
        
        frame = cv2.resize(frame, (new_width, new_height))
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time_end = time.perf_counter()
        time.sleep(max(1.0 / FPS - (time_end- time_start) / 1000, 0.0))
        

    cap.release()
    cv2.destroyAllWindows()
    audio_processor.stop()

if __name__ == "__main__":
    main()
