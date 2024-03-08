import cv2
import numpy as np
import io
import traceback
import json
import time
import util.logger as logger
from PIL import Image, ImageFont, ImageDraw
from image.text_translator import TextTranslator

class ImageProcessor:
    def __init__(self, azure_services):
        self.azure_services = azure_services
        self.text_translator = TextTranslator(self.azure_services)
        self.font = ImageFont.truetype("C:\\Windows\\Fonts\\msgothic.ttc", 25)
        self.last_process_frame_time = 0
        self.last_ocr_result = None
        

    def process_frame(self, frame):
        self.time_start = time.perf_counter()
        
        # フレームをPILイメージに変換
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # 480pに縮小して画像をAzureのOCRサービスに送信
        compressed_image, ratio = self.resize_image(image, (640, 480))
        logger.debug(f"image size: {ratio}")

        draw = ImageDraw.Draw(image)
        # PILイメージをバイト配列に変換
        byte_arr = io.BytesIO()
        compressed_image.save(byte_arr, format='PNG')
        image_binary = byte_arr.getvalue()
        image_buffer = io.BufferedReader(io.BytesIO(image_binary))

        if self.time_start - self.last_process_frame_time >= 10:
            self.last_process_frame_time = self.time_start

            ocr_result = self.azure_services.vision_client.recognize_printed_text_in_stream(image_buffer)
            self.last_ocr_result = ocr_result
            time_end = time.perf_counter()
            logger.info(f"ocr cost {time_end- self.time_start}s")
            logger.debug(ocr_result)
        else:
            ocr_result = self.last_ocr_result

        for region in ocr_result.regions:
            for line in region.lines:
                text = ' '.join([word.text for word in line.words])  # 単語を一文に結合
                left, top, width, height = [int(value) for value in line.bounding_box.split(",")]  # 文章全体のバウンディングボックスを取得
                nl, nt, nw, nh = [int(value / ratio) for value in [left, top, width, height]]
                logger.frame(f"Text: {text} ({left}, {top}, {width}, {height})")
                # 翻訳を実行
                translated_text = self.text_translator.translate(text, "en", "ja")
                
                logger.debug(f"ratio: {left}, {top}->{nl}, {nt}")
                # 翻訳したテキストを画像に描画
                bbox = draw.textbbox((nl, nt), translated_text, font=self.font)
                # 半透明の背景を作成
                overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
                draw_overlay = ImageDraw.Draw(overlay)
                draw_overlay.rectangle([(nl, nt), (nl+ bbox[2] - bbox[0], nt + bbox[3] - bbox[1])], fill=(0, 220, 255, 100))

                # 半透明の背景を元の画像に合成
                image = Image.alpha_composite(image.convert('RGBA'), overlay)

                draw = ImageDraw.Draw(image)
                
                draw.text((nl, nt), translated_text, font=self.font, fill=(255, 255, 255))

        # PILイメージをOpenCVの画像に変換
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        return frame
    
    # 画像をリサイズ 黒帯もやるよ
    def resize_image_with_tie(self, image, dist):
        ratio = min(dist[0] / image.size[0], dist[1] / image.size[1])

        resized_image = image.resize(new_size, Image.ANTIALIAS)
        new_image = Image.new('RGB', dist, (0, 0, 0))
        new_image.paste(resized_image, ((dist[0] - new_size[0]) // 2, (dist[1] - new_size[1]) // 2))

        return new_image

    def resize_image(self, image, dist):
        ratio = min(dist[0] / image.size[0], dist[1] / image.size[1])
        new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
        resized_image = image.resize(new_size, Image.LANCZOS)
        return resized_image, ratio 


