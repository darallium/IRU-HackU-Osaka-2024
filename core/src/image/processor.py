import cv2
import numpy as np
import io
import traceback
import json
import time
import asyncio
import threading
import util.logger as logger
from PIL import Image, ImageFont, ImageDraw
from image.overlay_text import OverlayText

class ImageProcessor:
    def __init__(self, azure_services, ocr_class, enable_resize=False):
        self.azure_services = azure_services
        self.overlay_text = OverlayText(self.azure_services)
        self.last_process_frame_time = 0
        self.last_ocr_result = None
        self.ocr_instance = ocr_class(self.azure_services)
        self.ocr_task = None
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()
        self.enable_resize = enable_resize

    def start_loop(self, loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

    async def recognize_text(self, image_buffer):
        return await self.ocr_instance.run(image_buffer)
    
    def process_frame(self, frame):
        self.time_start = time.perf_counter()
        
        # フレームをPILイメージに変換
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # 480pに縮小して画像をAzureのOCRサービスに送信
        ratio = 1.0
        if self.enable_resize:
            image, ratio, _ = self.resize_image(image, (640, 480))
            logger.frame(f"image size: {ratio}")

        # PILイメージをバイト配列に変換
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='PNG')
        image_binary = byte_arr.getvalue()
        image_buffer = io.BufferedReader(io.BytesIO(image_binary))

        if self.time_start - self.last_process_frame_time >= 10:
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
        ratio = min(dist[0] / image.size[0], dist[1] / image.size[1])
        new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
        resized_image = image.resize(new_size, Image.LANCZOS)
        return resized_image, ratio, new_size

    def resize_image_with_tie(self, image, dist):
        resized_image, _, new_size = self.resize_image(image, dist)
        new_image = Image.new('RGB', dist, (0, 0, 0))
        new_image.paste(resized_image, ((dist[0] - new_size[0]) // 2, (dist[1] - new_size[1]) // 2))
        return new_image