import cv2
import numpy as np
import io
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
        self.time_start = time.perf_counter()
        self.last_process_frame_time = 0
        self.last_ocr_result = None
        self.text_ocr_vision_ocr = TextOcrVisionOcr(self.azure_services)
        self.text_ocr_vision_read = TextOcrVisionRead(self.azure_services)
        self.ocr_task = None
        self.overlay_cache = None
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()

    def __del__(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        
    def start_loop(self, loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

    async def prepare_overlay_cache(self, frame):
        # 540pに縮小して画像をAzureのOCRサービスに送信
        ratio = 1.0
        if config.value_of("enable_datasaver"):
            resized_frame, ratio, _ = self.resize_image(frame, (960, 540))
            logger.frame(f"image size: {ratio}")
        else:
            resized_frame = frame

        _, buffer = cv2.imencode(".png", resized_frame)

        image_buffer = io.BufferedReader(io.BytesIO(buffer))

        if config.value_of("ocr_method") == "vision_read":
            ocr_instance  = self.text_ocr_vision_read
        elif config.value_of("ocr_method") == "vision_ocr":
            ocr_instance  = self.text_ocr_vision_ocr
            
        ocr_result = await ocr_instance.run(image_buffer)
        return self.overlay_text.draw_text(frame, ratio, ocr_result)
    
    def process_frame(self, frame):
        time_start = time.perf_counter()
        
        if config.value_of("always_ocr") and not self.ocr_task:
            self.ocr_task = asyncio.run_coroutine_threadsafe(self.prepare_overlay_cache(frame), self.loop)
            logger.info(f"new ocr task {self.ocr_task}")
            self.task_time_start = time.perf_counter()

        if not config.value_of("always_ocr") and time_start - self.last_process_frame_time >= config.value_of("ocr_interval"):
            
            if self.ocr_task and not self.ocr_task.done():
                logger.warning("old ocr task is not finished yet and will be canceled")
                self.ocr_task.cancel()

            if not self.ocr_task or (self.ocr_task and self.ocr_task.done()):
                self.last_process_frame_time = time_start
                self.ocr_task = asyncio.run_coroutine_threadsafe(self.prepare_overlay_cache(frame), self.loop)
                logger.info(f"new ocr task {self.ocr_task}")
                self.task_time_start = time.perf_counter()
            
        if self.ocr_task and self.ocr_task.done():
            self.overlay_cache = self.ocr_task.result()
            time_end = time.perf_counter()
            logger.info(f"ocr cost {time_end- self.task_time_start}s")
            self.ocr_task = None

        if self.overlay_cache is not None:
            frame = Image.fromarray(frame)
            frame = Image.alpha_composite(frame.convert('RGBA'), self.overlay_cache)
            frame = np.array(frame)

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
    
