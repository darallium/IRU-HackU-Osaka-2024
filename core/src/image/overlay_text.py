import cv2
import asyncio
import threading
import time
import numpy as np
import util.logger as logger
import util.config as config
from image.text_translator import TextTranslator
from PIL import Image, ImageDraw, ImageFont, ImageColor

class OverlayText:
    def __init__(self, azure_services):
        self.azure_services = azure_services
        self.text_translator = TextTranslator(self.azure_services)
        self.last_ocr_result = None
        self.text_image_buffer = None
        self.image_cache_task = None

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
        
    def prepare_image_cache(self, frame, ratio, ocr_result):
        self.text_translator.translate_ocr_result(ocr_result)
        text_image = Image.new('RGBA', (frame.shape[1], frame.shape[0]))
        if type(ocr_result) == self.azure_services.read_operation_result:
            for read_results in ocr_result.analyze_result.read_results:
                for line in read_results.lines:
                    text = line.text  # テキストを取得

                    # 翻訳を実行
                    translated_text = self.text_translator.translate(text, "en")
                    if translated_text[1] == config.value_of("target_language"):
                        continue

                    boundingBox = line.bounding_box#[int(i) for i in line.bounding_box]  # バウンディングボックスを取得
                    pts1 = np.float32([[boundingBox[i] / ratio, boundingBox[i+1] / ratio] for i in range(0,8,2)])  # バウンディングボックスから座標を取得
                    # width = max(np.linalg.norm(pts1[i]-pts1[(i+2)%4]) for i in range(0,4,2))  # 幅を計算
                    height = max(np.linalg.norm(pts1[i]-pts1[(i+3)%4]) for i in range(0,4,2))  # 高さを計算
                    font = ImageFont.truetype(self.font_path, height) #self.get_optimum_sized_font(translated_text[0], width, height)
                    d = ImageDraw.Draw(text_image)
                    if pts1[0] < pts1[4] and pts1[1] < pts1[5]:
                        d.rectangle([(pts1[0],pts1[1]), (pts1[4],pts1[5])], fill=(0, 0, 0))
                    elif pts1[0] > pts1[4] and pts1[1] > pts1[5]:
                        d.rectangle([(pts1[4],pts1[5]), (pts1[0],pts1[1])], fill=(0, 0, 0))

                    d.text((pts1[0],pts1[1]), translated_text[0], font=font, fill=(255, 255, 255))
        else:
            for region in ocr_result.regions:
                for line in region.lines:
                    text = ' '.join([word.text for word in line.words])  # 単語を一文に結合
                    # 翻訳を実行
                    translated_text = self.text_translator.translate(text, ocr_result.language)
                    if translated_text[1] == config.value_of("target_language"):
                        continue
                    left, top, width, height = [int(value) for value in line.bounding_box.split(",")]  # 文章全体のバウンディングボックスを取得
                    nl, nt, nw, nh = [int(value / ratio) for value in [left, top, width, height]]
                    font = self.get_optimum_sized_font(translated_text[0], nw, nh)
                    # 翻訳したテキストを半透明の背景を持つバッファに描画
                    d = ImageDraw.Draw(text_image)
                    d.rectangle([(nl, nt), (nl + nw, nt + nh)], fill=(0, 0, 0, config.value_of("overlay_alpha")))
                    d.text((int(nl), int(nt)), translated_text[0], font=font, fill=(255, 255, 255, 255))
        return text_image

    def draw_text(self, frame, ratio, ocr_result):
        self.font_path = config.value_of("font_path") 

        return self.prepare_image_cache(frame, ratio, ocr_result)
    
        
    def get_optimum_sized_font(self, text, width, height):
        font = ImageFont.truetype(self.font_path, height)
        img_dummy = Image.new('RGB', (1, 1))
        d_dummy = ImageDraw.Draw(img_dummy)
        bbox = d_dummy.textbbox((0, 0), text, font=font)
        if bbox[2] > width or bbox[3] > height:
            low, high = 1, height
            while low <= high:
                mid = (low + high) // 2
                font = ImageFont.truetype(self.font_path, mid)
                bbox = d_dummy.textbbox((0, 0), text, font=font)
                if bbox[2] <= width and bbox[3] <= height:
                    low = mid + 1
                else:
                    high = mid - 1
                    
        if font.size < 12:
            font = ImageFont.truetype(self.font_path, 12)
            logger.warning(f"font size is too small: {font.size}->{text}")

        return font
