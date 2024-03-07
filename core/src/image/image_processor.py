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
from image.text_translator import TextTranslator

class ImageProcessor:
    def __init__(self, azure_services, ocr_class):
        self.azure_services = azure_services
        self.text_translator = TextTranslator(self.azure_services)
        self.font = ImageFont.truetype("C:\\Windows\\Fonts\\msgothic.ttc", 25)
        self.last_process_frame_time = 0
        self.last_ocr_result = None
        self.ocr_instance = ocr_class(self.azure_services)
        self.ocr_task = None
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()

    def start_loop(self, loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

    async def recognize_text(self, image_buffer):
        return await self.ocr_instance.run(image_buffer)
    
    def process_frame(self, frame):
        self.time_start = time.perf_counter()
        
        # フレームをPILイメージに変換
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image)
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

        if ocr_result is None:
            return frame
        
        if ocr_result['analyzeResult']:
            for read_results in ocr_result['analyzeResult']['readResults']:
                for line in read_results['lines']:
                    print(f"Text: {line['text']}")
                    print(f"BoundingBox: {line['boundingBox']}")
        else:
            for region in ocr_result.regions:
                for line in region.lines:
                    text = ' '.join([word.text for word in line.words])  # 単語を一文に結合
                    left, top, width, height = [int(value) for value in line.bounding_box.split(",")]  # 文章全体のバウンディングボックスを取得
                    logger.frame(f"Text: {text} ({left}, {top}, {width}, {height})")
                    # 翻訳を実行
                    translated_text = self.text_translator.translate(text, "en", "ja")

                    # 翻訳したテキストを画像に描画
                    bbox = draw.textbbox((left, top), translated_text, font=self.font)
                    # 半透明の背景を作成
                    overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
                    draw_overlay = ImageDraw.Draw(overlay)
                    draw_overlay.rectangle([(left, top), (left + bbox[2] - bbox[0], top + bbox[3] - bbox[1])], fill=(0, 220, 255, 100))

                    # 半透明の背景を元の画像に合成
                    image = Image.alpha_composite(image.convert('RGBA'), overlay)

                    draw = ImageDraw.Draw(image)
                    
                    draw.text((left, top), translated_text, font=self.font, fill=(255, 255, 255))

        # PILイメージをOpenCVの画像に変換
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        return frame