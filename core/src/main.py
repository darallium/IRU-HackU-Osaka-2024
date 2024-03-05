# main.py
from image.azure_services import AzureServices
from image.image_processor import ImageProcessor
from audio.audio_processor import AudioProcessor
import cv2
import numpy as np
import time
import json

def main():

    with open('config.json', 'r') as f:
        config = json.load(f)

    azure_services = AzureServices(
        config['vision_key'],
        config['vision_endpoint'],
        config['translator_key'],
        config['translator_endpoint']
    )

    image_processor = ImageProcessor(azure_services)
    # audio_processor = AudioProcessor()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    width = 1920
    height = 1080
    FPS = 30
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    #capture.set(cv2.CAP_PROP_FPS, FPS)

    # audio_processor.start()

    while True:
        time_sta = time.perf_counter()
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imwrite("test_output_before.jpg", frame)
        frame = image_processor.process_frame(frame)
        cv2.imwrite("test_output_after.jpg", frame)

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
        print(f"cost {time_end- time_sta}s")
        # 実際に設定された解像度を取得
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f'Width: {width}, Height: {height}')
        time.sleep(10)

    cap.release()
    cv2.destroyAllWindows()
    # audio_processor.stop()

if __name__ == "__main__":
    main()