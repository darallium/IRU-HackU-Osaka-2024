import cv2
import numpy as np
import util.logger as logger
import util.config as config
from image.text_translator import TextTranslator
from PIL import Image, ImageDraw, ImageFont

class OverlayText:
    def __init__(self, azure_services):
        self.azure_services = azure_services
        self.text_translator = TextTranslator(self.azure_services)
        self.last_ocr_result = None
        self.text_image_buffer = None

    def draw_text(self, frame, ratio, ocr_result):
        self.font_path = config.value_of("font_path") 
        frame = Image.fromarray(frame)
        if self.last_ocr_result is not ocr_result:
            self.last_ocr_result = ocr_result
            self.text_image_buffer = Image.new('RGBA', (frame.width, frame.height))
            if type(ocr_result) == self.azure_services.read_operation_result:
                for read_results in ocr_result.analyze_result.read_results:
                    for line in read_results.lines:
                        text = line.text  # テキストを取得
                        boundingBox = [int(i) for i in line.bounding_box]  # バウンディングボックスを取得
                        pts1 = np.float32([[boundingBox[i] / ratio, boundingBox[i+1] / ratio] for i in range(0,8,2)])  # バウンディングボックスから座標を取得
                        width = max(np.linalg.norm(pts1[i]-pts1[(i+2)%4]) for i in range(0,4,2))  # 幅を計算
                        height = max(np.linalg.norm(pts1[i]-pts1[(i+3)%4]) for i in range(0,4,2))  # 高さを計算
                        
                        # 翻訳を実行
                        translated_text = self.text_translator.translate(text, "en")

                        font = self.get_optimum_sized_font(translated_text, width, height)

                        # 翻訳したテキストを半透明の背景を持つバッファに描画
                        img = Image.new('RGBA', (int(width), int(height)), (0, 0, 0, 100))
                        d = ImageDraw.Draw(img)
                        d.text((0,0), translated_text, font=font, fill=(255, 255, 255, 255))
                        img = np.array(img)

                        # 射影変換を用いてバッファを元の画像に描画
                        pts2 = np.float32([[0,0],[width,0],[width,height],[0,height]])
                        M = cv2.getPerspectiveTransform(pts2, pts1)
                        dst = cv2.warpPerspective(img, M, (frame.width, frame.height))
                        
                        # 元の画像とdstを合成
                        dst = Image.fromarray(dst)
                        self.text_image_buffer = Image.alpha_composite(self.text_image_buffer.convert('RGBA'), dst)
            else:
                for region in ocr_result.regions:
                    for line in region.lines:
                        text = ' '.join([word.text for word in line.words])  # 単語を一文に結合
                        left, top, width, height = [int(value) for value in line.bounding_box.split(",")]  # 文章全体のバウンディングボックスを取得
                        nl, nt, nw, nh = [int(value / ratio) for value in [left, top, width, height]]
                        # 翻訳を実行
                        translated_text = self.text_translator.translate(text, ocr_result.language)

                        font = self.get_optimum_sized_font(translated_text, nw, nh)

                        # 翻訳したテキストを半透明の背景を持つバッファに描画
                        d = ImageDraw.Draw(self.text_image_buffer)
                        d.rectangle([(nl, nt), (nl + nw, nt + nh)], fill=(0, 0, 0, 100))
                        d.text((int(nl), int(nt)), translated_text, font=font, fill=(255, 255, 255, 255))

        frame = Image.alpha_composite(frame.convert('RGBA'), self.text_image_buffer)
        frame = np.array(frame)
        return frame
        
    def get_optimum_sized_font(self, text, width, height):
        font = ImageFont.truetype(self.font_path, height)
        img_dummy = Image.new('RGBA', (1, 1))
        d_dummy = ImageDraw.Draw(img_dummy)
        bbox = d_dummy.textbbox((0, 0), text, font=font)
        if bbox[2] > width:
            low, high = 1, height
            while low <= high:
                mid = (low + high) // 2
                font = ImageFont.truetype(self.font_path, mid)
                bbox = d_dummy.textbbox((0, 0), text, font=font)
                if bbox[2] <= width:
                    low = mid + 1
                else:
                    high = mid - 1
        return font