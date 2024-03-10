import cv2
import numpy as np
import io
import traceback
import json
import time
import asyncio
import threading
import util.logger as logger
import util.config as config
from PIL import Image, ImageFont, ImageDraw
from image.overlay_text import OverlayText
from image.text_ocr.vision_ocr import TextOcrVisionOcr
from image.text_ocr.vision_read import TextOcrVisionRead

class ImageProcessor:
    def __init__(self, azure_services):
        self.azure_services = azure_services
        self.overlay_text = OverlayText(self.azure_services)
        self.last_process_frame_time = 0
        self.last_ocr_result = None
        self.text_ocr_vision_ocr = TextOcrVisionOcr(self.azure_services)
        self.text_ocr_vision_read = TextOcrVisionRead(self.azure_services)
        self.ocr_task = None
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()

    def start_loop(self, loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

    async def recognize_text(self, image_buffer):
        if config.value_of("ocr_method") == "vision_read":
            ocr_instance  = self.text_ocr_vision_read
        elif config.value_of("ocr_method") == "vision_ocr":
            ocr_instance  = self.text_ocr_vision_ocr
        return await ocr_instance.run(image_buffer)
    
    def process_frame(self, frame):
        self.time_start = time.perf_counter()
        
        # 480pに縮小して画像をAzureのOCRサービスに送信
        ratio = 1.0
        if config.value_of("enable_datasaver"):
            resized_frame, ratio, _ = self.resize_image(frame, (640, 480))
            logger.frame(f"image size: {ratio}")
        else:
            resized_frame = frame

        # PNG形式に変換
        _, buffer = cv2.imencode(".png", resized_frame)

        image_buffer = io.BufferedReader(io.BytesIO(buffer))

        if self.time_start - self.last_process_frame_time >= config.value_of("ocr_interval"):
            if self.ocr_task is not None:
                logger.warning("old ocr task is not finished yet and will be canceled")
                self.ocr_task.cancel()

            self.last_process_frame_time = self.time_start
            self.ocr_task = asyncio.run_coroutine_threadsafe(self.recognize_text(image_buffer), self.loop)
            logger.info(f"new ocr task {self.ocr_task}")

        if self.ocr_task and self.ocr_task.done():
            ocr_result = self.ocr_task.result()
            self.last_ocr_result = ocr_result
            time_end = time.perf_counter()
            logger.info(f"ocr cost {time_end- self.time_start}s")
            logger.debug(ocr_result)
            self.ocr_task = None
        else:
            ocr_result = self.last_ocr_result

        if ocr_result:
            frame = self.overlay_text.draw_text(frame, ratio, ocr_result)

        return frame
    
    def resize_image(self, image, dist):
        ratio = min(dist[0] / image.shape[1], dist[1] / image.shape[0])
        new_size = (int(image.shape[1] * ratio), int(image.shape[0] * ratio))
        resized_image = cv2.resize(image, new_size, interpolation = cv2.INTER_LANCZOS4)
        return resized_image, ratio, new_size

    def resize_image_with_tie(self, image, dist):
        resized_image, _, new_size = self.resize_image(image, dist)
        new_image = np.zeros((dist[1], dist[0], 3), np.uint8)
        new_image[(dist[1] - new_size[1]) // 2 : (dist[1] - new_size[1]) // 2 + new_size[1], 
                  (dist[0] - new_size[0]) // 2 : (dist[0] - new_size[0]) // 2 + new_size[0]] = resized_image
        return new_image
    