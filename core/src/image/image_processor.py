import cv2
import numpy as np
import io
import traceback
import json
from PIL import Image, ImageFont, ImageDraw
from image.text_translator import TextTranslator

class ImageProcessor:
    def __init__(self, azure_services):
        self.azure_services = azure_services
        self.text_translator = TextTranslator(self.azure_services)
        self.font = ImageFont.truetype("C:\\Windows\\Fonts\\msgothic.ttc", 25)

    def process_frame(self, frame):
        # フレームをPILイメージに変換
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image)
        # PILイメージをバイト配列に変換
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='PNG')
        image_binary = byte_arr.getvalue()
        image_buffer = io.BufferedReader(io.BytesIO(image_binary))
        ocr_result = self.azure_services.vision_client.recognize_printed_text_in_stream(image_buffer)
        print(ocr_result)
        for region in ocr_result.regions:
            print(region)
            for line in region.lines:
                text = ' '.join([word.text for word in line.words])  # 単語を一文に結合
                left, top, width, height = [int(value) for value in line.bounding_box.split(",")]  # 文章全体のバウンディングボックスを取得
                print(text, left, top, width, height)
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